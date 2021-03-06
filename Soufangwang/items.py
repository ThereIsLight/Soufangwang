# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ResoldHouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 17个字段
    name = scrapy.Field()
    price = scrapy.Field()
    aver = scrapy.Field()
    build_time = scrapy.Field()
    area = scrapy.Field()  # 建筑面积
    house_type = scrapy.Field()
    floor = scrapy.Field()
    subdistrict = scrapy.Field()
    community = scrapy.Field()
    address = scrapy.Field()  # 搜房网没有地址
    source = scrapy.Field()
    link = scrapy.Field()
    decoration = scrapy.Field()
    orientation = scrapy.Field()
    build_type = scrapy.Field()  # 都在建筑类别中
    structure = scrapy.Field()  # 都在建筑类别中
    use = scrapy.Field()  # 对应着住宅类别


class NewHouseItem(scrapy.Item):
    #16个字段
    name = scrapy.Field()
    aver = scrapy.Field()
    around_aver = scrapy.Field()
    house_type = scrapy.Field()
    use = scrapy.Field()
    developer = scrapy.Field()
    subdistrict = scrapy.Field()
    address = scrapy.Field()
    status = scrapy.Field()
    start_time = scrapy.Field()
    give_time = scrapy.Field()
    use_num = scrapy.Field()
    company = scrapy.Field()
    build_type = scrapy.Field()
    source = scrapy.Field()
    link = scrapy.Field()
    # name, aver, around_aver, house_type, use, developer, subdistrict, address, status, start_time, give_time, use_num, company, build_type , source, link
