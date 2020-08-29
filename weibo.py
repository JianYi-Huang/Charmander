#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
    FileName : weibo.py
    Date : 2020/08/28 00:19:59
    Author : HuangJianYi
    Copyright : © 2020 HuangJianYi <vahx@foxmail.com>
    License : MIT, see LICENSE for more details.
"""

import datetime
import http.client
import json
import re
import time
import urllib

import requests
from bs4 import BeautifulSoup


def get_config(id="all"):
    with open("C:/JianYi-Huang/config.json", "r") as config:
        result = json.load(config)
        if id == "all":
            return result
        else:
            try:
                return result[id]
            except:
                return result["error"] + id


config = get_config("pushover")
def pushover(msg=None):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request(
        "POST",
        "/1/messages.json",
        urllib.parse.urlencode(
            {
                "token": config["token"],
                "user": config["user"],
                # "title": "这是一个标题",
                "message": msg,
            }
        ),
        {"Content-type": "application/x-www-form-urlencoded"},
    )
    conn.getresponse()


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
}

cookies = {
    "cookies": "SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5ff6F7iFj6sE1L2v511-G.; SUB=_2AkMoHw0zf8NxqwJRmf8RxG3jZY9-yQjEieKeQ_zoJRMxHRl-yj9jqkMZtRB6A58j3CcvF79rkvA7lOcOp4Ica6bGk1OJ; login_sid_t=611a5bcf4bed078a006ff618d8100b21; cross_origin_proto=SSL; Ugrow-G0=cf25a00b541269674d0feadd72dce35f; YF-V5-G0=7a7738669dbd9095bf06898e71d6256d; WBStorage=70753a84f86f85ff|undefined; _s_tentry=passport.weibo.com; Apache=2971103865920.6855.1598259723500; SINAGLOBAL=2971103865920.6855.1598259723500; ULV=1598259723506:1:1:1:2971103865920.6855.1598259723500:; wb_view_log=1920*10801; YF-Page-G0=8a1a69dc6ba21f1cd10b039dff0f4381|1598259895|1598259710"
}

# url_1 = input ( "请输入微博博主的url:" + str() )
last_time = int(
    time.mktime(time.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d"))
)  # 获取就今天0点0分0秒的时间戳
weibo_data = {}

while True:
    # url = 'https://weibo.com/u/7230522444?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=1#feedtop'
    url = "https://weibo.com/u/7230522444?is_all=1" # 运势学家王明磊
    req = requests.get(url, headers=headers, cookies=cookies)
    print('resp:', req.ok)
    req = req.text
    detail = re.findall(r"WB_detail(.*?)WB_like", req, re.I)  # WB_detail

    # for i in detail:
    i = detail[0]
    weibo_data["datetime"] = re.search(
        r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", i, re.I
    ).group()  # 日期和时间

    nickname = re.search(r'nick-name=\\"(.*?)\\">', i, re.I).group()
    nickname = nickname.replace('nick-name=\\"', "")  # 删除nick-name=\"
    weibo_data["nickname"] = nickname.replace('\\">', "")  # 删除\"> #博主名称

    weibotext = re.search(r'nick-name=\\"(.*?)<\\/div>', i, re.I).group()
    weibotext = re.search(r">\\n(.*?)<\\/div>", weibotext, re.I).group()
    weibotext = weibotext.replace(" ", "")  # 删除空格
    weibotext = weibotext.replace(">\\n", "")  # 删除>\n
    weibotext = weibotext.replace("<\\/div>", "")  # 删除<\/div>
    weibo_data["weibotext"] = weibotext.replace("<br>", "\n")  # <br>替换换行

    new_time = int(time.mktime(time.strptime(weibo_data["datetime"], "%Y-%m-%d %H:%M")))
    new_msg = (
        weibo_data["nickname"]
        + " "
        + weibo_data["datetime"]
        + "\n"
        + weibo_data["weibotext"]
    )
    if new_time > last_time:
        pushover(new_msg)
        last_time = new_time
        print('今日运程播报获取成功,已推送到手机上,请查看!!')
    else:
        print('监控中! 最近一次更新时间:', weibo_data['datetime'])
    time.sleep(60)
    # try:
    #     time.sleep(5)
    # except Exception as e:
    #     print (e)
    #     pass
