import re

http = re.compile("http")
L = [
    "https://dongfangyingduwdqd.fang.com/",
    "/house/dianshang/huangdao/"
]
for l in L:
    if re.match(http, l):
        print('nihao1')