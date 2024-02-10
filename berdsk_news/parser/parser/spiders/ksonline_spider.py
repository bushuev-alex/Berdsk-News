import datetime
# import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime  #, timedelta


class KSOnlineSpider(scrapy.Spider):
    name: str = "ksonline"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = ["https://ksonline.ru/category/news//",
                  "https://ksonline.ru/category/news/page/2/",
                  # "https://ksonline.ru/category/news/page/3/",
                  ]

    async def parse(self, response, **kwargs):
        news_list = response.css("div.td_module_16.td_module_wrap")

        for news in news_list:
            try:
                full_text_link: str = news.css("h3.entry-title a::attr(href)").get()
                published_at: str = news.css("div.td-module-meta-info time::attr(datetime)").get()
                news_info: dict = await self.get_news_info(link=full_text_link)

                yield {"author": news.css("div.td-post-author-name a::text").get(),
                       "title": news.css("div h3.entry-title a::text").get(),  # название
                       "brief_text": news.css("div.td-excerpt p::text").get(),  # короткое описание
                       "full_text": news_info.get("full_text"),  # полный текст
                       "title_image_url": news_info.get("title_image_url"),  # изображение у заглавия
                       "images_urls": news_info.get("images_urls"),  # строка с ссылками на фото в статье
                       "tag_list": news_info.get("tag_list"),  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": news_info.get("search_words"),  # строка всех тегов
                       "category_list": news_info.get("category_list"),
                       "parsed_from": "ksonline.ru",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": datetime.fromisoformat(published_at.replace("+00:00", "+07:00")),
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
            full_text_list: list[soup] = soup.find("div", {"class": "td-post-content"}).findAll("p")

            title_image_url = soup.find("div", {"class": "td-post-featured-image"}).find("img").get("srcset")

            images_urls_list: list = [p.find("img").get("src") for p in full_text_list if p.find("img")]
            tag_list: list[soup] = soup.find("ul", {"class": "td-tags"}).findAll("li")
            category: list[soup] = soup.find("ul", {"class": "td-category"}).findAll("li")
            return {"full_text": "XYWZ".join((p.text.strip() if not p.find("em") else "" for p in full_text_list)),
                    "title_image_url": title_image_url.split(" ")[-2].strip(),
                    "tag_list": [tag.text.strip().capitalize() for tag in tag_list[1:]],  # [1:] - удаляем слово ТЭГ
                    "category_list": [cat.text.strip().capitalize() for cat in category],
                    "images_urls": " ".join(images_urls_list)
                    }
