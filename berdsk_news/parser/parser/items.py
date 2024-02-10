# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserItem(scrapy.Item):
    author = scrapy.Field()
    title = scrapy.Field()
    brief_text = scrapy.Field()
    full_text = scrapy.Field()
    title_image_url = scrapy.Field()
    images_urls = scrapy.Field()
    tag = scrapy.Field()
    search_words = scrapy.Field()
    category = scrapy.Field()
    parsed_from = scrapy.Field()
    full_text_link = scrapy.Field()
    published_at = scrapy.Field()
    parsed_at = scrapy.Field()
