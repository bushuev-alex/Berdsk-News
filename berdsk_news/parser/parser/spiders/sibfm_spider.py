import datetime
# import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime  #, timedelta


class SibFmSpider(scrapy.Spider):
    name: str = "sibfm"
    headers: dict = {"Origin": "https://sib.fm",
                     "Referer": "https://sib.fm/publications/news",
                     'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = ["https://sib.fm/",
                  # "https://sib.fm/publications/news/",
                  # "https://sib.fm/last/publications/next/",
                  # "https://sib.fm/last/publications/next/",
                  ]

    today = datetime.today()

    async def parse(self, response, **kwargs):
        news_list = response.css("div.news-side__item")

        for news in news_list:
            try:
                base_url = "https://sib.fm"
                full_text_link: str = base_url + news.css("div.news-side__text a.text::attr('href')").get()
                time: str = news.css("div.news-side__date::text").get()[-5:]
                news_info: dict = await self.get_news_info(link=full_text_link)

                yield {"author": news_info.get("author"),
                       "title": news.css("div.news-side__text a.text::text").get(),  # название
                       "brief_text": news_info.get("brief_text"),  # короткое описание
                       "full_text": news_info.get("full_text"),  # полный текст
                       "title_image_url": news_info.get("title_image_url"),  # изображение у заглавия
                       "images_urls": news_info.get("images_urls"),  # строка с ссылками на фото в статье
                       "tag_list": news_info.get("tag_list"),  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": news_info.get("search_words"),  # строка всех тегов
                       "category_list": news_info.get("category_list"),
                       "parsed_from": "sib.fm",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": datetime.fromisoformat(f"{self.today.year}-"
                                                              f"{'%02d' % self.today.month}-"
                                                              f"{self.today.day}"
                                                              f"T{time}:00"),
                       "parsed_at": datetime.utcnow(),  # дата добавления / парсинга
                       }
            except AttributeError as e:
                print(e, full_text_link)
                continue
            except IndexError as e:
                print(e, full_text_link)
                continue
            except TypeError as e:
                print(e, full_text_link)
                continue

    async def get_news_info(self, link: str) -> dict:
        res = requests.get(url=link, headers=self.headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            full_text_list: list[soup] = soup.find("div", {"class": "content-article__text"}).findAll("p")
            title_image_url = soup.find("div", {"class": "header-article__image"}).find("img").get("src")
            author = soup.find("p", {"class": "author-text"}).find("a")
            categories = soup.find("div", {"class": "header-article__tags"}).find("a")
            return {
                "author": author.text.strip().split("\n")[0],
                "brief_text": full_text_list[0].text,
                "full_text": "XYWZ".join((p.text.strip() for p in full_text_list[1:])),
                "title_image_url": title_image_url,
                "category_list": [categories.text.strip().capitalize()],
                "images_urls": " "
            }
