import datetime
import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime, timedelta


class BerdskOnlineSpider(scrapy.Spider):
    name: str = "b_online"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    today = datetime.today()
    yesterday = today - timedelta(days=3)

    start_urls = [f"https://berdsk-online.ru/news/?date-start={yesterday.year}-{yesterday.month}-{yesterday.day}"
                  f"&date-finish={today.year}-{today.month}-{today.day}",
                  # f"https://berdsk-online.ru/news/?date-start={2024}-{03}-{15}&date-finish={2024}-{03}-{17}",
                  ]

    async def parse(self, response, **kwargs):
        news_list = response.css('div.news_list a')

        for news in news_list:
            try:
                full_text_link: str = news.css('a::attr(href)').get()
                news_info: dict = await self.get_news_info(link=full_text_link)

                yield {"author": news_info.get("author"),
                       "title": news.css('div.news_block_name::text').get(),  # название
                       "brief_text": news.css('div.news_block_txt::text').get(),  # короткое описание
                       "full_text": news_info.get("full_text"),  # полный текст
                       "title_image_url": news.css("div.news_block_img img::attr(data-lazy-src)").get(),
                       "images_urls": news_info.get("images_urls"),  # список ссылок на фото в статье
                       "tag_list": news_info.get("tag_list"),  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": news_info.get("search_words"),  # строка всех тегов
                       "category_list": news_info.get("category_list"),
                       "parsed_from": "berdsk-online.ru",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": datetime.strptime(news_info.get("published_at"), "%d.%m.%Y %H:%M"),
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
            full_text_list: list[soup] = soup.find("div", {"class": "news_detail_slide_news_txt"}).findAll("p")
            author = soup.find("div", {"class": "field-avtor"}).find("a")
            categories = soup.find("div", {"class": "news_detail_slide_news_region"}).find('a')
            tags = soup.find("div", {"class": "tag-list"})
            published_at = soup.find("div", {"class": "news_detail_slide_news_date"}).text
            return {
                "author": re.split(r"[.|,] ", author.text.strip())[0],
                "full_text": "XYWZ".join((p.text.strip() for p in full_text_list)),
                "category_list": [category.text.strip() for category in categories],
                "tag_list": [tags.text.strip().capitalize()],
                "images_urls": await self.get_all_images(full_text_list),
                "published_at": published_at,
            }

    async def get_all_images(self, full_text_list: list) -> str:
        try:
            figures = [p.find("img").get("data-lazy-src-webp") for p in full_text_list if p.find("img")]
            imgs = " ".join(figures)
            return imgs
        except TypeError as e:
            print(e)
        except IndexError as e:
            print(e)
