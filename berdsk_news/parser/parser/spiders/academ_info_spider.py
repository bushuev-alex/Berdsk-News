import datetime
import json

# import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime  # , timedelta


class AcademInfoSpider(scrapy.Spider):
    name: str = "academinfo"
    base_url = "https://academ.info"
    headers: dict = {"Referer": "https://academ.info/news/",
                     'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = ["https://academ.info/news/",
                  # "https://academ.info/news/?PAGEN_1=2",
                  ]

    async def parse(self, response, **kwargs):
        news_list = response.css("div.grid-list__item")

        for news in news_list:
            try:
                full_text_link: str = self.base_url + news.css("div.items-list-inner__item-title a::attr(href)").get()
                news_info: dict = await self.get_news_info(link=full_text_link)

                yield {"author": None,
                       "title": news.css("div.items-list-inner__item-title a::text").get(),  # название
                       "brief_text": news.css("div.items-list-inner__item-preview::text").get().strip(),
                       "full_text": news_info.get("full_text"),  # полный текст
                       "title_image_url": news_info.get("title_image_url"),  # изображение у заглавия
                       "images_urls": news_info.get("images_urls"),  # список ссылок на фото в статье
                       "tag_list": news_info.get("tag_list"),  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": news_info.get("search_words"),  # строка всех тегов
                       "category_list": [news.css("div.review-list-inner__label a::text").get()],
                       "parsed_from": "academ.info",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": datetime.fromisoformat(news_info.get("published_at")),  # дата публикации
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

            script_content = soup.findAll("script")[3]
            script_content_js: dict = json.loads(str(script_content.contents[0]))

            full_text_list: list[soup] = soup.find("div", {"class": "content"}).findAll("p")
            title_image_url = soup.find("div",
                                        {"class": "detail-image detail-image--left"}).find("img").get("src")
            try:
                images_urls_list: list[soup] = soup.find("div", {"class": "gallery-small"}).findAll("img")
                images_urls: list = [(self.base_url + img.get("src")) for img in images_urls_list]
            except AttributeError:
                images_urls: list = []

            return {"full_text": "XYWZ".join((p.text.strip() for p in full_text_list)),
                    "title_image_url": self.base_url + title_image_url,
                    "images_urls": " ".join(images_urls),
                    "published_at": script_content_js.get("datePublished").strip()
                    }

