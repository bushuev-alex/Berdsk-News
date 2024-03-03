import datetime
import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime, timedelta


class NGSSpider(scrapy.Spider):
    name: str = "ngs"
    headers: dict = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/116.0.5845.1028 YaBrowser/23.9.1.1028 (beta) Yowser/2.5 Safari/537.36"}

    today = datetime.today()
    yesterday = today - timedelta(days=1)

    start_urls = [f"https://ngs.ru/text/?dateFrom={yesterday.day}.{yesterday.month}.{yesterday.year}"
                  f"&dateTo={today.day}.{today.month}.{today.year}&page=1",
                  f"https://ngs.ru/text/?dateFrom={yesterday.day}.{yesterday.month}.{yesterday.year}"
                  f"&dateTo={today.day}.{today.month}.{today.year}&page=2",
                  f"https://ngs.ru/text/?dateFrom={yesterday.day}.{yesterday.month}.{yesterday.year}"
                  f"&dateTo={today.day}.{today.month}.{today.year}&page=3",
                  f"https://ngs.ru/text/?dateFrom={yesterday.day}.{yesterday.month}.{yesterday.year}"
                  f"&dateTo={today.day}.{today.month}.{today.year}&page=4",
                  f"https://ngs.ru/text/?dateFrom={yesterday.day}.{yesterday.month}.{yesterday.year}"
                  f"&dateTo={today.day}.{today.month}.{today.year}&page=5",
                  f"https://ngs.ru/text/?dateFrom={yesterday.day}.{yesterday.month}.{yesterday.year}"
                  f"&dateTo={today.day}.{today.month}.{today.year}&page=6",
                  ]

    async def parse(self, response, **kwargs):
        target_script_content = response.css("script")[39].get()
        raw_urls: list[str] = re.findall(
            pattern=r"urlCanonical\":\"(https:\\u002F\\u002Fngs.ru\\u002F"
                    r"text\\u002F\w+\\u002F\d{4}\\u002F\d{2}\\u002F\d{2}\\u002F\d{8}\\u002F)\",",
            string=target_script_content)
        # 1st var: r"\\u002Ftext\\u002F\w+"\\u002F\d{4}\\u002F\d{2}\\u002F\d{2}\\u002F\d{8}",

        links = [url.replace("\\u002F", "/") for url in raw_urls]
        print(links)

        for link in links:
            try:
                full_text_link: str = link  # = "https://ngs.ru" + link + "/"
                news_info: dict = await self.get_news_info(link=full_text_link)

                yield {"author": news_info.get("author"),
                       "title": news_info.get("title"),  # название
                       "brief_text": news_info.get("brief_text"),  # короткое описание
                       "full_text": news_info.get("full_text"),  # полный текст
                       "title_image_url": news_info.get("title_image_url"),  # изображение у заглавия
                       "images_urls": news_info.get("images_urls"),  # строка с ссылками на фото в статье
                       "tag_list": news_info.get("tag_list"),  # тэг - тема новости (первое слово/фраза из группы тегов)
                       "search_words": news_info.get("search_words"),  # строка всех тегов
                       "category_list": news_info.get("category_list"),
                       "parsed_from": "ngs.ru",  # название сайта
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
            title = soup.find("h1", {"itemprop": "headline"}).text
            brief_text = soup.find("p", {"itemprop": "alternativeHeadline"}).text
            title_image_url = soup.find("div", {"itemprop": "articleBody"}).find("img").get("src")
            published_at = soup.find("meta", {"itemprop": "datePublished"}).get("content")
            author = soup.find("div", {"itemprop": "author"}).find("p", {"itemprop": "name"}).text
            categories = soup.find("li", {"itemprop": "itemListElement"}).find("a")
            return {
                "author": author,
                "title": title,
                "brief_text": brief_text,
                "full_text": await self.get_full_text(soup),
                "title_image_url": title_image_url,
                "tag_list": await self.get_tag_list(soup),
                "category_list": [categories.find("span").text.strip().capitalize()],
                "images_urls": await self.get_all_images(soup),
                "published_at": published_at
            }

    async def get_all_images(self, soup: BeautifulSoup) -> str:
        figures = soup.findAll("figure", {"itemscope": "itemscope"})
        imgs = " ".join([fig.find("img").get("src") for fig in figures[1:] if fig.find("img")])
        return imgs

    async def get_full_text(self, soup: BeautifulSoup) -> str:
        full_text_list: list[soup] = soup.find("div", {"itemprop": "articleBody"}).findAll("p")
        full_text_list_ = []
        for p in full_text_list:
            exclude_conditions = (p.find("span"),
                                  p.get("itemprop") == "author",
                                  "Поделиться" in p.text,
                                  )
            if any(exclude_conditions):
                continue
            full_text_list_.append(p.text.strip())
        return "XYWZ".join(full_text_list_)

    async def get_tag_list(self, soup: BeautifulSoup) -> list:
        tags_list = []
        tags: list[soup] = soup.findAll("a")
        for a in tags:
            try:
                if "tags" in a.get("href"):
                    tags_list.append(a.get("title"))
            except TypeError:
                continue
        return tags_list
