import datetime
import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime, timedelta


class NSUSpider(scrapy.Spider):
    name: str = "nsu"
    headers: dict = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
                               "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                     'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
                     "sec-ch-ua-platform": "Linux",
                     }
    base_url = "https://www.nsu.ru"
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    day_ago = today - timedelta(days=3)

    start_urls = [
        f"https://www.nsu.ru/n/media/news/"
        f"?newsFilter_DATE_ACTIVE_FROM_1={day_ago.day}.{day_ago.month}.{day_ago.year}"
        f"&newsFilter_DATE_ACTIVE_FROM_2={tomorrow.day}.{tomorrow.month}.{tomorrow.year}"
        f"&set_filter=Найти&set_filter=Y"
    ]

    async def parse(self, response, **kwargs):
        news_list = response.css('div.news-card')

        for news in news_list:
            try:
                full_text_link: str = news.css('a::attr(href)').get()
                if not full_text_link.startswith("https"):
                    full_text_link = "https://www.nsu.ru" + full_text_link
                news_info: dict = await self.get_news_info(link=full_text_link)

                yield {"author": news_info.get("author"),
                       "title": news.css('a.name::text').get(),  # название
                       "brief_text": news.css('p::text').get().strip(),  # короткое описание
                       "full_text": news_info.get("full_text"),  # полный текст
                       "title_image_url": self.base_url + news.css("a.img-wrap img::attr(src)").get(),
                       "images_urls": news_info.get("images_urls", ""),  # список ссылок на фото в статье
                       "tag_list": news_info.get("tag_list"),  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": news_info.get("search_words"),  # строка всех тегов
                       "category_list": news_info.get("tag_list"),  # category_list = tag_list
                       "parsed_from": "nsu.ru",  # название сайта
                       "full_text_link": full_text_link,  # ссылка на полный текст
                       "published_at": datetime.utcnow(),  # дата публикации =  дата добавления / парсинга
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

            try:
                author_ = soup.find("div", {"class": "property"}).text
                author = " ".join(re.split(r"[ |(,)]", author_)[2:4]).strip()
            except Exception as e:
                author = "Пресс-служба НГУ"

            tags = soup.find("div", {"class": "tags"}).findAll("a", {"class": "tag-item"})
            return {
                "author": author,
                "full_text": await self.get_full_text(soup),
                "tag_list": [tag.text.strip() for tag in tags],
                "images_urls": await self.get_all_images(soup),
            }

    async def get_all_images(self, soup: BeautifulSoup) -> str:
        try:
            figures = soup.find("div", {"class": "news-silder"}).findAll("div", {"class": "item"})
            imgs = " ".join([self.base_url + fig.find("img").get("src") for fig in figures])
            return imgs
        except TypeError as e:
            print(e)
        except IndexError as e:
            print(e)

    async def get_full_text(self, soup: BeautifulSoup):
        full_text_list = soup.find("div", {"class": "detail_text"}).findAll("p")
        if full_text_list:
            full_text = "XYWZ".join([p.text.strip() for p in full_text_list])
        else:
            full_text_list = soup.find("div", {"class": "detail_text"}).text.split("\n")
            full_text = "XYWZ".join([p.strip() for p in full_text_list if p])
        return full_text
