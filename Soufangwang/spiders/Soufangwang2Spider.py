import scrapy
import re
import logging
from scrapy.http import Request
from Soufangwang.items import ResoldHouseItem
"""
2017年4月6日15:42:39
第一次运行，基本上顺利完成。没有遇到搜房网反爬虫措施。
缺点：
    1.极少部分的网页不对，例如第一个属性name在绝大部分网页中是/html/body/div[8]/div[2]/div[3]/div[1]/h1/text()，
    少部分是div[9]其他的属性可能也有变化。
    2.有一些网页的年代属性没有数字，但是现在已经改正。
    3.在很多的网页中，build_type and structure是混为一谈的。
    4.Filtered duplicate request: <GET http://esf.qd.fang.com/chushou/3_185195156.htm> - no more duplicates will be shown (see DUPEFILTER_DEBUG to show all duplicates)
    遇到这个提示，大概是因为请求的网址相同，就会自动的过滤掉。也许是因为搜房网一些的房屋信息都是重复的。
2017年4月6日18:46:52
运行完成，还是极有个别的网页出错，但是暂时不想改了，获取到的数据够多了。成功获取2700+条数据。
"""


class SoufangwangS2pider(scrapy.Spider):

    name = "soufangwang2"
    allowed_domains = ['esf.qd.fang.com']
    domain_url = "http://esf.qd.fang.com"
    head_url = 'http://esf.qd.fang.com/house-a01142/i3'  # 貌似时通过i3后面的数字来选择page_url
    # 第一个网页地址 http://esf.qd.fang.com/house-a01142/i31/
    # 最后一个网页地址 http://esf.qd.fang.com/house-a01142/i3100/

    def start_requests(self):
        start_url = self.head_url + '1/'
        yield Request(start_url, callback=self.parse)

    def parse(self, response):
        max_num = response.xpath("//*[@id='list_D10_15']/span/text()").extract()[0]  # 共100页
        max_num = re.findall(r'\d+', max_num)[0]
        for i in range(1, int(max_num) + 1):
        # for i in range(1, 2):  # test
            page_url = self.head_url + str(i) + "/"
            # print(page_url)
            yield Request(page_url, callback=self.get_link, dont_filter=True)

    def get_link(self, response):
        """
        这里可以获取房屋的具体地址,但是没什么用.
        :param response:
        :return:
        """

        dls = response.xpath("/html/body/div[4]/div[4]/div[4]/dl")
        for dl in dls:
            info_url = dl.xpath("dt/a/@href").extract()[0]  # 这里的info_url的格式为/chushou/3_185706299.htm
            info_url = self.domain_url + info_url
            address = dl.xpath("dd/p[3]/span/text()").extract()[0]  # 格式为西海岸CBD商圈-滨海大道与朝阳路交汇处，是区域与地址的结合
            address = address.split('-')[1]
            # print(info_url, address)
            yield Request(info_url, callback=self.get_info, meta={'address': address})
        '''
        dl = response.xpath("/html/body/div[4]/div[4]/div[4]/dl")
        info_url = dl.xpath("dt/a/@href").extract()[0]  # 这里的info_url的格式为/chushou/3_185706299.htm
        info_url = self.domain_url + info_url
        address = dl.xpath("dd/p[3]/span/text()").extract()[0]  # 格式为西海岸CBD商圈-滨海大道与朝阳路交汇处，是区域与地址的结合
        address = address.split('-')[1]
        print(info_url, address)
        yield Request(info_url, callback=self.get_info, meta={'address': address})
        '''
    def get_info(self, response):

        item = ResoldHouseItem()
        re_num = re.compile(r"\d+\.?\d*")

        # 这几个属性的位置基本上是固定的，暂时不用去考虑。
        name = response.xpath("//div[@class='main clearfix']/div[3]/div[1]/h1/text()").extract()[0].strip()
        price = response.xpath("//div[@class='main clearfix']/div[3]/div[2]/div[2]/dl[1]/dt/span[2]/text()").extract()[0]  # 直接是数字
        aver = response.xpath("//div[@class='main clearfix']/div[3]/div[2]/div[2]/dl[1]/dt/text()[3]").extract()[0]  # 需要提取数字
        aver = re.findall(re_num, aver)[0]
        area = response.xpath("//div[@class='main clearfix']/div[3]/div[2]/div[2]/dl[1]/dd[4]/span/text()").extract()[0]
        area = re.findall(re_num, area)[0]
        house_type = response.xpath("//div[@class='main clearfix']/div[3]/div[2]/div[2]/dl[1]/dd[3]/text()").extract()[0]
        subdistrict = response.xpath("//div[@class='main clearfix']/div[3]/div[2]/div[2]/dl[2]/dt[1]/a[3]/text()").extract()[0].strip()
        community = response.xpath("//div[@class='main clearfix']/div[3]/div[2]/div[2]/dl[2]/dt[1]/a[1]/text()").extract()[0].strip()
        address = response.meta['address']
        source = '搜房网'
        link = response.url

        # 一下几个属性的位置不是固定的，甚至少数网页连名称都不是固定的。网页中电话下面属性的位置全都不是固定的。
        # 都怪那些别墅
        decoration = '暂无数据'
        build_type = '暂无数据'
        structure = '暂无数据'  # 在搜房网中build_type structure都放在一个属性'建筑类别'中了。
        use = '别墅'
        floor = '暂无数据'
        build_time = 0
        orientation = '暂无数据'

        dds = response.xpath("//div[@class='main clearfix']/div[3]/div[2]/div[2]/dl[2]/dd")
        for dd in dds:
            d = dd.xpath('span')
            span = d.xpath('string(.)').extract()[0].strip('：')
            if span == '装修' or span == '装修程度':
                decoration = dd.xpath('text()[2]').extract()[0]
            elif span == '建筑类别' or span == '建筑形式':
                build_type = dd.xpath('text()[2]').extract()[0]
            elif span == '住宅类别':
                use = dd.xpath('text()[2]').extract()[0]
            elif span == '楼层' or span == '地上层数':
                floor = dd.xpath('text()[2]').extract()[0]
            elif span == '建筑年代' or span == '年代':
                build_time = dd.xpath('text()[2]').extract()[0]
                build_time = re.findall(re_num, build_time)
                if build_time:
                    build_time = build_time[0]
                else:
                    build_time = 0
            elif span == '进门朝向' or span == '朝向':
                orientation = dd.xpath('text()[2]').extract()[0]
            else:
                pass
        '''
        print('长长长长长长长长长长长长长长长长长长长长的分割线')
        print('name', name)
        print('price', price)
        print('aver', aver)
        print('build_time', build_time)
        print('subdistrict', subdistrict)
        print('community', community)
        print('address', address)
        print('source', source)
        print('link', link)
        print('area', area)
        print('house_type', house_type)
        print('floor', floor)
        print('decoration', decoration)
        print('orientation', orientation)
        print('build_type', build_type)
        print('structure', structure)
        print('use', use)
        # 最后统一将字符串转化为数字
        '''
        item['name'] = name
        item['price'] = float(price)
        item['aver'] = float(aver)
        item['build_time'] = build_time
        item['subdistrict'] = subdistrict
        item['community'] = community
        item['source'] = source
        item['address'] = address
        item['link'] = link
        item['area'] = float(area.strip('㎡'))
        item['house_type'] = house_type
        item['floor'] = floor
        item['decoration'] = decoration
        item['orientation'] = orientation
        item['build_type'] = build_type
        item['structure'] = structure
        item['use'] = use
        # self.logger.info(item)
        yield item

