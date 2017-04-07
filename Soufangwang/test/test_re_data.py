import re

data = [
    '',
    '暂无资料',
    '2017年3月26日开盘',
    '预计2018年8月交房',
    '3月18日开盘',
    '2016年6月底加推B2-B4号楼',
    '2016年4月23日已加推4号楼',
    '预计2016年9、10月开盘销售',  # 故居这个时最麻烦的。
    '48#于2016年6月18日开盘',
    '预计2018年',
]
re_year = re.compile(r"\d{4}年")
re_year_month = re.compile(r"\d{4}年\d{1,2}月")
re_year_month_date = re.compile(r"\d{4}年\d{1,2}月\d{1,2}日")
re_year_month_optional = re.compile(r"\d{4}年\d{1,2}月\d{1,2}日|\d{4}年\d{1,2}月|\d{4}年|\d{1,2}月\d{1,2}日")

# 可以进行匹配判断
def get_correct_start_time(str):
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

def get_correct_give_time(str):
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
def get_correct_format(str):
    if str == '暂无数据':
        return str
    else:
        L = re.findall(r"\d+", str)
        if len(L[1]) <= 1:
            L[1] = '0' + L[1]
        if len(L[2]) <= 1:
            L[2] = '0' + L[2]
        return "-".join(L)

for d in data:
    # print(get_correct_start_time(d))
    # print(get_correct_give_time(d))
    print(get_correct_format(get_correct_start_time(d)))
