# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter
import psycopg
from psycopg.errors import UniqueViolation
import scrapy
from .settings import DB_LOGIN, DB_PASS, DB_NAME, DB_HOST, DB_PORT, ORIGINS

ORIGINS = json.loads(ORIGINS)

# from django.db import connection


class ParserPipeline:

    def __init__(self):
        self.connection = psycopg.connect(user=DB_LOGIN,
                                          password=DB_PASS,
                                          host=DB_HOST,
                                          port=DB_PORT,
                                          dbname=DB_NAME)
        self.cur = self.connection.cursor()

    def process_item(self, item, spider):

        origin_id = self.fill_origin(item, spider)
        author_id = self.fill_author(origin_id, item, spider)

        query = """SELECT id FROM news_news WHERE title = %s"""
        self.cur.execute(query, (item['title'],))
        news_id = self.cur.fetchone()

        if news_id:
            news_id = news_id[0]
            spider.logger.warn(f"Item {item['title']} is already in table news_news with ID={news_id}")
        else:
            stmt = """INSERT INTO news_news (
                author_id, title, brief_text, full_text, title_image_url, images_urls, search_words, 
                parsed_from_id, full_text_link, published_at, parsed_at, rating
                 )  
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING ID"""
            self.cur.execute(stmt,
                             (author_id, item.get('title'), item.get('brief_text'), item.get('full_text'),
                              item.get('title_image_url'), item.get('images_urls'),  # item.get('tag'),
                              item.get('search_words'), origin_id,  # item.get('category'),
                              item.get('full_text_link'), item.get('published_at'), item.get('parsed_at'), 0))
            news_id = self.cur.fetchone()[0]
            spider.logger.warn("********** " + item.get('title') +
                               f" is successfully added to table news_news with ID={news_id}! **********")

            self.fill_news_newscategory(news_id, item, spider)
            if spider.name != "sibfm":
                self.fill_news_newstag(news_id, item, spider)
            spider.logger.warn(f"Table news_newscategory is filled with values")

        return item

    def fill_news_newscategory(self, news_id, item, spider):
        category_list = item['category_list']

        for category in category_list:

            if not category:
                continue
            elif category == "Новости":
                category = "Общество"

            query = """SELECT id FROM news_category WHERE name = %s"""
            self.cur.execute(query, (category,))
            cat_id = self.cur.fetchone()

            if cat_id:
                cat_id = cat_id[0]
                spider.logger.warn(f"Category {category} is already in table news_category with ID={cat_id}")
            else:
                stmt = """INSERT INTO news_category (name, rating) VALUES (%s, %s) RETURNING id"""
                self.cur.execute(stmt, (category, 0))
                cat_id = self.cur.fetchone()[0]
                spider.logger.warn(f"NEW category {category} in news_category with ID={cat_id}")

            query = """SELECT id FROM news_newscategory WHERE news_id = %s AND category_id = %s"""
            self.cur.execute(query, (news_id, cat_id,))
            news_newscat_id = self.cur.fetchone()

            if news_newscat_id:
                spider.logger.warn(f"A pair with cat_id={cat_id} and news_id={news_id} is already exists.")
                continue
            else:
                stmt = """INSERT INTO news_newscategory (news_id, category_id) VALUES (%s, %s)"""
                self.cur.execute(stmt, (news_id, cat_id))
                self.connection.commit()
                spider.logger.warn(f"A new pair added to news_newscategory with cat_id={cat_id}, news_id={news_id}.")

    def fill_news_newstag(self, news_id, item, spider):
        try:
            tag_list = item['tag_list']

            for tag in tag_list:

                if not tag:
                    continue
                elif tag == "ТЭГ":
                    tag = "регион"

                query = """SELECT id FROM news_tag WHERE name = %s"""
                self.cur.execute(query, (tag,))
                tag_id = self.cur.fetchone()

                if tag_id:
                    tag_id = tag_id[0]
                    spider.logger.warn(f"Tag {tag} is already in table news_tag with ID={tag_id}")
                else:
                    stmt = """INSERT INTO news_tag (name, rating) VALUES (%s, %s) RETURNING id"""
                    self.cur.execute(stmt, (tag, 0))
                    tag_id = self.cur.fetchone()[0]
                    spider.logger.warn(f"NEW tag {tag} in news_tag with ID={tag_id}")

                query = """SELECT id FROM news_newstag WHERE news_id = %s AND tag_id = %s"""
                self.cur.execute(query, (news_id, tag_id,))
                news_newstag_id = self.cur.fetchone()

                if news_newstag_id:
                    spider.logger.warn(f"A pair with tag_id={tag_id} and news_id={news_id} is already exists.")
                    continue
                else:
                    stmt = """INSERT INTO news_newstag (news_id, tag_id) VALUES (%s, %s)"""
                    self.cur.execute(stmt, (news_id, tag_id))
                    self.connection.commit()
                    spider.logger.warn(f"A new pair added to news_newstag with tag_id={tag_id}, news_id={news_id}.")
            return True
        except TypeError as e:
            print(e, "there is NO tag in item")
            return False

    def fill_origin(self, item, spider):
        parsed_from = item.get("parsed_from")

        query = """SELECT id FROM news_origin WHERE base_url = %s"""
        self.cur.execute(query, (parsed_from,))
        origin_id = self.cur.fetchone()

        if origin_id:
            origin_id = origin_id[0]
            spider.logger.warn(f"Origin {parsed_from} is already in table news_origin with ID={origin_id}")
        else:
            stmt = """INSERT INTO news_origin (name, base_url, rating) VALUES (%s, %s, %s) RETURNING id"""
            self.cur.execute(stmt, (ORIGINS.get(parsed_from), parsed_from, 0))
            origin_id = self.cur.fetchone()[0]
            spider.logger.warn(f"NEW origin {parsed_from} in news_origin with ID={origin_id}")

        return origin_id

    def fill_author(self, origin_id, item, spider):
        author = item.get('author')
        if not author:
            author = "Редакция"

        fio = author.split()
        if len(fio) == 1:
            first_name, last_name = fio[0], ""
        elif len(fio) == 2:
            first_name, last_name = fio[0], fio[1]

        query = """SELECT id FROM news_author 
                WHERE first_name = %s AND last_name = %s AND work_at_id = %s"""
        self.cur.execute(query, (first_name, last_name, origin_id))
        author_id = self.cur.fetchone()

        if author_id:
            author_id = author_id[0]
            spider.logger.warn(f"Author {author} is already in table news_author with ID={author_id}")
        else:
            stmt = """INSERT INTO news_author (first_name, last_name, work_at_id, rating) 
                        VALUES (%s, %s, %s, %s) RETURNING id"""
            self.cur.execute(stmt, (first_name, last_name, origin_id, 0))
            author_id = self.cur.fetchone()[0]
            spider.logger.warn(f"NEW author {author} added to news_author with ID={author_id}")
        return author_id

    def close_spider(self, spider: scrapy.Spider = None):  # , spider=None, reason=None
        self.cur.close()
        self.connection.close()
