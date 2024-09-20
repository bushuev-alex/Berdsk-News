import datetime
import json

# import re

from bs4 import BeautifulSoup
import requests
import scrapy
from datetime import datetime  # , timedelta


class AcademInfoSpider(scrapy.Spider):
    name: str = "academinfo"
    base_url: str = "https://academ.info"
    headers: dict = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
                               "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                     "Accept-Encoding": "gzip, deflate, br, zstd",
                     'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                   "Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
                     "Referer": "https://academ.info/news/?PAGEN_1=2",
                     "Cookie": "_ym_debug=null; scroll_block=null; _ym_uid=1693631394390615044; "
                               "adtech_uid=61336ad4-ba51-47c2-9ce4-b5313907fd47%3Aacadem.info; _ym_d=1711187398; "
                               "top100_id=t1.7685730.747803947.1722695285209; beget=begetok; _ga=GA1.1.863834965.1724166611;"
                               " "
                               "BX_USER_ID=7eb99dbbc4a602ad0f54e2fa4611ce38; tmr_lvid=075530c4775067db18a536a963f39d9f; "
                               "tmr_lvidTS=1693631394013; domain_sid=PffTnYB340EEP_OIPUv5-%3A1726381092336; "
                               "_ac_oid=cbcc7eec63a09fa33505e87aa5e5eba0%3A1726388470964; "
                               "_ga_X5NR8KKRSN=GS1.1.1726498933.7.0.1726498933.0.0.0; _ym_debug=null; scroll_block=null; "
                               "PHPSESSID=7070dd5505168af1750ed778715b3455; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A5%2"
                               "C%22EXPIRE%22%3A1726765140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; "
                               "t3_sid_7685730=s1.834295303.1726759296749.1726760789872.17.48",
                     }
    cookies: dict = {"_ym_debug": "null",
                     "scroll_block": "null",
                     "_ym_uid": "1693631394390615044",
                     "adtech_uid": "61336ad4-ba51-47c2-9ce4-b5313907fd47%3Aacadem.info",
                     "_ym_d": "1711187398",
                     "top100_id": "t1.7685730.747803947.1722695285209",
                     "beget": "begetok",
                     "_ga": "GA1.1.863834965.1724166611",
                     "BX_USER_ID": "7eb99dbbc4a602ad0f54e2fa4611ce38",
                     "tmr_lvid": "075530c4775067db18a536a963f39d9f",
                     "tmr_lvidTS": "1693631394013",
                     "domain_sid": "PffTnYB340EEP_OIPUv5-%3A1726381092336",
                     "_ac_oid": "cbcc7eec63a09fa33505e87aa5e5eba0%3A1726388470964",
                     "_ga_X5NR8KKRSN": "GS1.1.1726498933.7.0.1726498933.0.0.0",
                     "PHPSESSID": "7070dd5505168af1750ed778715b3455",
                     "BITRIX_CONVERSION_CONTEXT_s1": "%7B%22ID%22%3A5%2C%22EXPIRE%22%3A1726765140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D",
                     "t3_sid_7685730": "s1.834295303.1726759296749.1726760789872.17.48",
                     }

    start_urls = ["https://academ.info/news/",
                  "https://academ.info/news/?PAGEN_1=2",
                  ]

    def start_requests(self):
        if not self.start_urls and hasattr(self, "start_url"):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)"
            )
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, dont_filter=False)

    async def parse(self, response, **kwargs):
        # res = requests.get(url=self.start_urls[0], headers=self.headers)
        # request = scrapy.Request(url=self.start_urls[0])
        # print(response.text)
        news_list = response.css("div.items-list-inner div.grid-list__item")
        for news in news_list:
            try:
                full_text_link: str = self.base_url + news.css("div.items-list-inner__item-title a::attr(href)").get()
                news_info: dict = await self.get_news_info(link=full_text_link)
                # print(news_info)
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
