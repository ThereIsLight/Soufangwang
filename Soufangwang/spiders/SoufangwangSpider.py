import scrapy
import re
import logging
from scrapy.http import Request
from Soufangwang.items import NewHouseItem
from bs4 import BeautifulSoup

class SoufangwangSpider(scrapy.Spider):
    """
    使用之前看看页数有没有变化。
    """
    name = 'soufangwang'
    # allowed_domains = ['newhouse.qd.fang.com']  # 一些网址不在这个范围内
    head_url = 'http://newhouse.qd.fang.com/house/s/huangdao/b9'

    def start_requests(self):
        # for i in range(1, 2):
        for i in range(1, 8):  # test
            page_url = self.head_url + str(i) + '/'
            yield Request(page_url, callback=self.parse)

    def parse(self, response):
        re_http = re.compile("http")
        tags = response.xpath("//div[@class='nlcd_name']/a")
        for a in tags:
            info_url = a.xpath('@href').extract()[0]
            # 第一个页面的第一个房屋信息是自营房产。获取到的链接不对。格式为/house/dianshang/huangdao/,并且补完网址之后，会跳转到自营房产索引界面。
            if re.match(re_http, info_url):  #是以http开头,自营房产不考虑了。
                yield Request(info_url, callback=self.get_details, dont_filter=True)
                # break  # test
                # print(info_url)

    def get_details(self, response):
        """
        需要获取楼盘详情的地址
        :param response:
        :return:
        """
        detail_url = response.xpath("//div[@class='navleft tf']/a[2]/@href").extract()[0]
        # print(detail_url)
        yield Request(detail_url, self.get_info)

    def get_info(self, response):
        """
        由于网页代码的问题，这里不能使用XPath(某些地方返回值为空)，只能使用Beautifulsoup。
        绝大部分网页的结构都是类似的。但是少数写字楼的网页结构不一样。先暂且不用管，存到数据库后，再去观察数据的具体结构。
        :param response:
        :return:
        """

        item = NewHouseItem()
        re_num = re.compile(r"\d+\.?\d*")
        soup = BeautifulSoup(response.text, 'lxml')

        # 初始化 貌似各个属性的位置是固定的。很遗憾属性的位置不是固定的。写字楼的属性位置与其他的房屋不同。
        name = "暂无数据"
        aver = 0  # 当无法提取到数字时，就为0
        around_aver = 0  # around_aver永远是0
        house_type = "暂无数据"
        use = "暂无数据"
        developer = "暂无数据"
        subdistrict = "暂无数据"  # 在网页中没有找到对应的数据
        address = "暂无数据"
        status = "暂无数据"
        start_time = "暂无数据"
        give_time = "暂无数据"
        use_num = '暂无数据'
        company = "暂无数据"
        build_type = "暂无数据"
        source = "搜房网"
        link = response.url

        # 获取属性值。首先将网页分为写字楼与非写字楼两类，分别获取。
        # 其次，非写字楼的某些网页某些属性的位置也会不同。例如build_type，developer
        name = soup.find('div', id='daohang').find('a', class_='ts_linear').get_text()
        aver = soup.find_all('div', class_='main-item')[0].find('div', class_='main-info-price').find('em').get_text().strip()
        use = soup.find_all('div', class_='main-item')[0].find_all('li')[0].find_all('div')[1].get_text().strip()
        if use == '写字楼':
            # house_type
            developer = soup.find_all('div', class_='main-item')[0].find_all('li')[6].find_all('div')[1].get_text()
            address = soup.find_all('div', class_='main-item')[0].find_all('li')[6].find_all('div')[1].get_text().strip()
            status = soup.find_all('div', class_='main-item')[1].find_all('li')[0].find_all('div')[1].get_text().strip()
            start_time = soup.find_all('div', class_='main-item')[1].find_all('li')[2].find_all('div')[1].get_text()
            give_time = soup.find_all('div', class_='main-item')[1].find_all('li')[3].find_all('div')[1].get_text()
            # use_num
            company = soup.find_all('div', class_='main-item')[4].find_all('li')[0].find_all('div')[1].get_text()
            # build_type
        elif use == '住宅底商' or use == '市场类商铺' or use == '购物中心':  # 大约也就是五六个网页，真烦！！！
            # house_type
            developer = soup.find_all('div', class_='main-item')[0].find_all('li')[5].find_all('div')[1].get_text()
            address = soup.find_all('div', class_='main-item')[0].find_all('li')[7].find_all('div')[1].get_text().strip()
            status = soup.find_all('div', class_='main-item')[1].find_all('li')[0].find_all('div')[1].get_text().strip()
            start_time = soup.find_all('div', class_='main-item')[1].find_all('li')[2].find_all('div')[1].get_text()
            give_time = soup.find_all('div', class_='main-item')[1].find_all('li')[3].find_all('div')[1].get_text()
            # use_num
            company = soup.find_all('div', class_='main-item')[4].find_all('li')[0].find_all('div')[1].get_text()
            # build_type
        else:
            house_type = soup.find_all('div', class_='main-item')[1].find_all('li', class_='list-text')[0].find_all('div')[1].get_text()  # 貌似是get_text()可以获得当前标签与子标签的内容。
            developer = soup.find_all('div', class_='main-item')[0].find_all('li', class_='list-text')[0].find('a').get_text()
            address = soup.find_all('div', class_='main-item')[0].find_all('li', class_='list-text')[1].find_all('div')[1].get_text().strip()
            status = soup.find_all('div', class_='main-item')[1].find_all('li')[0].find_all('div')[1].get_text().strip()
            start_time = soup.find_all('div', class_='main-item')[1].find_all('li')[2].find_all('div')[1].get_text()
            give_time = soup.find_all('div', class_='main-item')[1].find_all('li')[3].find_all('div')[1].get_text()
            use_num = soup.find_all('div', class_='main-item')[3].find_all('li')[6].find_all('div')[1].get_text()
            company = soup.find_all('div', class_='main-item')[3].find_all('li')[7].find_all('div')[1].get_text()
            build_type = soup.find_all('div', class_='main-item')[0].find_all('li')[2].find_all('div')[1].find('span').get_text()

        # 对属性值进行处理。对日期的处理放在管道中，因为太过于复杂了，放在这里使程序的结构很乱。
        aver = re.findall(re_num, aver)
        if aver:
            aver = float(aver[0])
        else:
            aver = 0
        house_type = "，".join(house_type.split())
        build_type = "，".join(build_type.split())
        use_num = re.findall(re_num, use_num)
        if use_num:
            use_num = float(use_num[0])
        else:
            use_num = 0
        '''
        print('name', name)
        print('aver', aver)
        print('around_aver', around_aver)
        print('use', use)
        print('developer', developer)
        print('subdistrict', subdistrict)
        print('address', address)
        print('house_type', house_type)
        print('status', status)
        print('start_time', start_time)
        print('give_time', give_time)
        print('use_num', use_num)
        print('company', company)
        print('build_type', build_type)
        print('source', source)
        print('link', link)
        '''
        item['name'] = name
        item['aver'] = aver
        item['around_aver'] = around_aver
        item['house_type'] = house_type
        item['use'] = use
        item['developer'] = developer
        item['subdistrict'] = subdistrict
        item['address'] = address
        item['status'] = status
        item['start_time'] = start_time
        item['give_time'] = give_time
        item['use_num'] = use_num
        item['company'] = company
        item['build_type'] = build_type
        item['source'] = source
        item['link'] = link
        yield item