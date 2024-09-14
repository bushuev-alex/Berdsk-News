import datetime
import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime, timedelta


class NGSSpider(scrapy.Spider):
    name: str = "ngs"
    headers: dict = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
                               "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                     'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
                     "Cookie": "jtnews_ab_24=A; jtnews_ab_29=A; _ym_uid=1666349083772181309; "
                               "tildauid=1683954093151.379824; jtnews_crookie_reset=true; "
                               "jtnews_ab_main_page_4redesign=B; adrcid=ANKX-rQDygCxFwUYJsu6oGQ; "
                               "jtnews_a_template=true; __ddg1_=qQY8OJVC7Jc58rNkAGls; _ym_d=1698024866; "
                               "ngs_uid=wxPcGWVgugKG//JXBNyfAg==; ngs_analytics_uid=wxPcEmVh0cxuFr/xInqoAg==; "
                               "an_h_uid=12DC13C3CCD16165F1BF166E02A87A22; ump_ab_v1=legacy; __ddgid_=3qoHphFn2NEIYwLw; "
                               "__ddg2_=hFDmW2Dm7FCG2ncP; ump_ab_v2=legacy; _ga_1937V52Y9V=GS1.2.1709868734.10.0.1709868734.0.0.0; "
                               "_ga=GA1.1.403770720.1680981391; ump_ab_v3=ump; "
                               "crookie=AyEilT4x2OQnaFh4/sInI3b+j4rRSD++pUQFpmGRRe1jVAiT/Fyvf9ZgZ/Ah7TtuyJP7FdsQ9OjxapRAGkwc8PzDuYQ=; "
                               "cmtchd=MTcxMDY3NDg4MTIxMg; _ym_isad=1; _ym_visorc=w; __ddgmark_=eiTckPVQbpPh0Iah; "
                               "__ddg5_=tQ8LEHSuSzebFrji; ngs_sid=985879739cadfcc7c94cd8d808bab830; "
                               "_ga_KRPLCP05GH=GS1.1.1710879056.422.1.1710883516.0.0.0",
                     }

    today = datetime.today()
    yesterday = today - timedelta(days=1)

    start_urls = [f"https://ngs.ru/text/?dateFrom={yesterday.day}.{yesterday.month}.{yesterday.year}"
                  f"&dateTo={today.day}.{today.month}.{today.year}&page=1",
                  # f"https://ngs.ru/text/?dateFrom={yesterday.day}.{yesterday.month}.{yesterday.year}"
                  # f"&dateTo={today.day}.{today.month}.{today.year}&page=2",
                  # f"https://ngs.ru/text/?dateFrom={yesterday.day}.{yesterday.month}.{yesterday.year}"
                  # f"&dateTo={today.day}.{today.month}.{today.year}&page=3",
                  # f"https://ngs.ru/text/?dateFrom={yesterday.day}.{yesterday.month}.{yesterday.year}"
                  # f"&dateTo={today.day}.{today.month}.{today.year}&page=4",
                  # f"https://ngs.ru/text/?dateFrom={yesterday.day}.{yesterday.month}.{yesterday.year}"
                  # f"&dateTo={today.day}.{today.month}.{today.year}&page=5",
                  # f"https://ngs.ru/text/?dateFrom={yesterday.day}.{yesterday.month}.{yesterday.year}"
                  # f"&dateTo={today.day}.{today.month}.{today.year}&page=6",
                  ]

    async def parse(self, response, **kwargs):
        target_script_content = response.css("script")[36].get()
        raw_urls: list[str] = re.findall(
            pattern=r"urlCanonical\":\"(https:\\u002F\\u002Fngs.ru\\u002F"
                    r"text\\u002F\w+\\u002F\d{4}\\u002F\d{2}\\u002F\d{2}\\u002F\d{8}\\u002F)\",",
            string=target_script_content)
        # 1st var: r"\\u002Ftext\\u002F\w+"\\u002F\d{4}\\u002F\d{2}\\u002F\d{2}\\u002F\d{8}",

        links = [url.replace("\\u002F", "/") for url in raw_urls]
        # print(links)

        for link in links:
            try:
                full_text_link: str = link  # = "https://ngs.ru" + link + "/"
                news_info: dict = await self.get_news_info(link=full_text_link)

                yield {"author": news_info.get("author"),
                       "title": news_info.get("title"),
                       "brief_text": news_info.get("brief_text"),
                       "full_text": news_info.get("full_text"),
                       "title_image_url": news_info.get("title_image_url"),
                       "images_urls": news_info.get("images_urls"),
                       "tag_list": news_info.get("tag_list"),
                       "search_words": news_info.get("search_words"),
                       "category_list": news_info.get("category_list"),
                       "parsed_from": "ngs.ru",
                       "full_text_link": full_text_link,
                       "published_at": datetime.fromisoformat(news_info.get("published_at")),
                       "parsed_at": datetime.utcnow(),
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
        # print(res.status_code)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'lxml')
            title = soup.find("h1", {"itemprop": "headline"}).text
            brief_text = soup.find("p", {"itemprop": "description alternativeHeadline"}).text
            try:
                title_image_url = soup.find("div", {"itemprop": "articleBody"}).find("img").get("src")
            except AttributeError as e:
                print(e)
                title_image_url = " "
            published_at = soup.find("meta", {"itemprop": "datePublished"}).get("content")
            author = soup.find("div", {"itemprop": "name"}).find("a", {"itemprop": "url"}).text
            categories = soup.find("span", {"itemprop": "itemListElement"})  # .find("a")
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
        figures = soup.find("div", {"itemprop": "articleBody"}).findAll("picture")
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
                    tags_list.append(a.text.strip())
            except TypeError:
                continue
        return tags_list
