from Soufangwang.items import NewHouseItem
from .sql_soufangwang import SoufangwangSQL
import logging
import re

re_year = re.compile(r"\d{4}年")
re_year_month = re.compile(r"\d{4}年\d{1,2}月")
re_year_month_date = re.compile(r"\d{4}年\d{1,2}月\d{1,2}日")

class SoufangwangPipeline(object):

    logger = logging.getLogger()

    def get_correct_start_time(self, str):
        flag = re.findall(re_year_month_date, str)
        if flag:
            return flag[0]
        else:
            flag = re.findall(re_year_month, str)
            if flag:
                return flag[0] + '1日'
            else:
                flag = re.findall(re_year, str)
                if flag:
                    return flag[0] + '1月' + '1日'
                else:
                    return '暂无数据'

    def get_correct_give_time(self, str):
        flag = re.findall(re_year_month_date, str)
        if flag:
            return flag[0]
        else:
            flag = re.findall(re_year_month, str)
            if flag:
                return flag[0] + '30日'
            else:
                flag = re.findall(re_year, str)
                if flag:
                    return flag[0] + '12月' + '30日'
                else:
                    return '暂无数据'

    def get_correct_format(self, str):
        if str == '暂无数据':
            return str
        else:
            L = re.findall(r"\d+", str)
            if len(L[1]) <= 1:
                L[1] = '0' + L[1]
            if len(L[2]) <= 1:
                L[2] = '0' + L[2]
            return "-".join(L)

    def process_item(self, item, spider):

        self.logger.info('come into anjuke pipeline!!!!!!!!!!!!!!!!!!')
        if isinstance(item, NewHouseItem):
            name = item['name']
            aver = item['aver']
            around_aver = item['around_aver']
            house_type = item['house_type']
            use = item['use']
            developer = item['developer']
            subdistrict = item['subdistrict']
            address = item['address']
            source = item['source']
            link = item['link']
            status = item['status']
            start_time = self.get_correct_format(self.get_correct_start_time(item['start_time']))
            # start_time = item['start_time']
            give_time = self.get_correct_format(self.get_correct_give_time(item['give_time']))
            # give_time = item['give_time']
            use_num = item['use_num']
            company = item['company']
            build_type = item['build_type']
            self.logger.info('start to execute sql........................')
            SoufangwangSQL.insert_data(name, aver, around_aver, house_type, use, developer, subdistrict, address, status,
                                  start_time, give_time, use_num, company, build_type , source, link)

