"""
作者：sagegrass
程序名：高等学校信息爬取
联系方式：sagegrass@outlook.com
创建时间：2022-06-03
更新时间：2022-06-03
"""

import requests
import re
import json
import time
from lxml import etree

school = list()
num = 0

try:
    while True:
        url = f"https://gaokao.chsi.com.cn/sch/search--ss-on,option-qg,searchType-1,start-{num}.dhtml"
        r = requests.get(url, headers={"user-agent": "Mozilla 5.0"}, timeout=10)

        for s in (t := etree.HTML(r.text).xpath("//table[@class='ch-table']/tr")[1::]):
            if len(t) <= 1:
                break
            school.append({"院校名称": re.sub("\s", "", s.xpath("./td[1]/a/text()")[0] if len(s.xpath("./td[1]/a/text()")) else s.xpath("./td[1]/text()")[0]),
                    "院校所在地": re.sub("\s", "", s.xpath("./td[2]/text()")[0]),
                    "教育行政主管部门": re.sub("\s", "", s.xpath("./td[3]/text()")[0]),
                    "学历层次": re.sub("\s", "", s.xpath("./td[4]/text()")[0]),
                    "双一流建设高校": "是" if len(s.xpath("./td[5]/i/text()")) else "否",
                    "研究生院": "是" if len(s.xpath("./td[6]/i/text()")) else "否",
                    "满意度": re.sub("\s", "", s.xpath("./td[7]/a/text()")[0]) if len(s.xpath("./td[7]/a/text()")) > 0 else "--"})
        else:
            num += 20
            print(f"已经完成{num}个学校啦！")
            time.sleep(1)
            continue
        print("恭喜，已经全部完成了！")
        assert(False)
except Exception as e:
    with open("院校记录.json", "w") as f:
        f.write(json.dumps(school, indent=2, ensure_ascii=False))
    if not isinstance(e, AssertionError):
        raise

