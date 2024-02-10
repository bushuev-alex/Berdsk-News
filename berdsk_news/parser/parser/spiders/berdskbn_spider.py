import datetime
# import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime  # , timedelta


class BerdskBNSpider(scrapy.Spider):
    name: str = "berdskbn"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    start_urls = ["https://berdsk-bn.ru/category/novosti/page/1/",
                  "https://berdsk-bn.ru/category/obshestvo/page/1/",
                  "https://berdsk-bn.ru/category/politica/page/1/",
                  "https://berdsk-bn.ru/category/nacproekty/page/1/",
                  "https://berdsk-bn.ru/category/accident/page/1/",
                  "https://berdsk-bn.ru/category/ekonomica/page/1/",
                  ]

    async def parse(self, response, **kwargs):
        news_list = response.css("div.col")

        for news in news_list:
            try:
                full_text_link: str = news.css("div h2.entry-title a::attr(href)").get()
                published_at: str = news.css("div.entry-meta a time.published::attr(datetime)").get()
                news_info: dict = await self.get_news_info(link=full_text_link)

                yield {"author": news.css("div.entry-meta span.author a::text").get(),
                       "title": news.css("div h2.entry-title a::text").get(),  # название
                       "brief_text": news.css("div.entry-summary p::text").get(),  # короткое описание
                       "full_text": news_info.get("full_text"),  # полный текст
                       "title_image_url": news_info.get("title_image_url"),  # изображение у заглавия
                       "images_urls": news_info.get("images_urls"),  # список ссылок на фото в статье
                       "tag_list": news_info.get("tag_list"),  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": news_info.get("search_words"),  # строка всех тегов
                       "category_list": news_info.get("category_list"),
                       "parsed_from": "berdsk-bn.ru",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": datetime.fromisoformat(published_at),  # дата публикации
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
            full_text_list: list[soup] = soup.find("div", {"class": "entry-content"}).findAll("p")
            title_image_url = await self.get_best_images(soup, "title")
            # title_image_url = soup.find("div", {"class": "post-thumbnail"}).find("img").get("srcset")
            images_urls = await self.get_best_images(soup, "gallery")
            tags: list[soup] = soup.find("div", {"class": "nd-post-body"}).findAll("a", {"rel": "tag"})
            categories: list[soup] = soup.find("div", {"class": "nd-post-body"}).find("span").findAll("a")
            return {"full_text": "XYWZ".join((p.text.strip() if not p.find("em") else "" for p in full_text_list)),
                    "title_image_url": title_image_url,
                    "tag_list": set(tag.text.strip().capitalize() for tag in tags),
                    "category_list": [cat.text.strip().capitalize() for cat in categories],
                    "images_urls": " ".join(images_urls)
                    }

    async def get_best_images(self, soup: BeautifulSoup, photo_type: str):
        try:
            if photo_type == "gallery":
                images_figure_tags = (soup.find("div", {"class": "entry-content"}).
                                      findAll("figure", {"class": "wp-block-image"}))
                images_urls_list = [fig.find("img").get("srcset") for fig in images_figure_tags]
                img_urls = []
                img_urls += [sorted([url_.split() for url_ in images_urls.split(", ")],
                                    key=lambda x: int(x[1][:-1]),
                                    reverse=True)[0][0]
                             for images_urls in images_urls_list]
                return img_urls
            elif photo_type == "title":
                images_urls = soup.find("div", {"class": "post-thumbnail"}).find("img").get("srcset")
                if images_urls:
                    img_url: str = sorted([url_.split() for url_ in images_urls.split(", ")],
                                          key=lambda x: int(x[1][:-1]),
                                          reverse=True)[0][0]
                else:
                    img_url = soup.find("div", {"class": "post-thumbnail"}).find("img").get("src")
                return img_url.strip()

        except TypeError:
            return ""
        except IndexError:
            return ""
