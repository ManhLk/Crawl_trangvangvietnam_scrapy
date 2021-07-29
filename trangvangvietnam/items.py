# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    tax_code = scrapy.Field()
    established_at = scrapy.Field()
    introduce = scrapy.Field()
    industry = scrapy.Field()
    product = scrapy.Field()
    website = scrapy.Field()
    email = scrapy.Field()
    address = scrapy.Field()
    phone_number = scrapy.Field()
    fax = scrapy.Field()
    created_at = scrapy.Field()
