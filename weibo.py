import requests
from bs4 import BeautifulSoup
import json
import re
import time

#1:使用正则表达之去除html标签
def filter_tags(htmlstr):
#先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    s=s.replace('网页链接','')
    return s


headers = {'user-agent':
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
          }
          
cookies = {'cookies':
           'Ugrow-G0=6fd5dedc9d0f894fec342d051b79679e; login_sid_t=397ddbbec81e4d92cc79209732ed1d4b; cross_origin_proto=SSL; YF-V5-G0=7a7738669dbd9095bf06898e71d6256d; _s_tentry=passport.weibo.com; wb_view_log=1920*10801; Apache=1846385593775.2017.1598063291201; SINAGLOBAL=1846385593775.2017.1598063291201; ULV=1598063291206:1:1:1:1846385593775.2017.1598063291201:; WBtopGlobal_register_version=434eed67f50005bd; YF-Page-G0=580fe01acc9791e17cca20c5fa377d00|1598064777|1598064677; SUB=_2A25yRPynDeRhGeBJ6lMX9SrFzTSIHXVRMGlvrDV8PUNbmtANLVnSkW9NRkqfSyDtRj8kkT8y4LiUqmKj00MedsFg; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5YoUfCPzcZHUhr.fjoVC4-5JpX5KzhUgL.FoqNeK2cSKB4Son2dJLoIE-LxK-LBo5L12qLxKqLBo-LBKeLxKML1hqL122LxK-L1K5L1Kq_; SUHB=0S7SNyMxpwTyzG; ALF=1629601911; SSOLoginState=1598065912'
          }

# url_1 = input ( "请输入微博博主的url:" + str() ) 


i = 1
count = 1
while True:
    # url = url_1 + '&page=' + str(i)
    url = 'https://weibo.com/u/7230522444?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=0#feedtop'
    # req = requests.get(url, headers=headers, cookies=cookies).text
    req = requests.get(url, headers=headers).text
    re_script = re.compile('nick-name(.*?)div',re.I) # Script
    re_br = re.compile('<br\s*?/?>') # 处理换行
    m = re_script.findall(req)
    # soup = BeautifulSoup(req, 'html.parser')
    new_list = []
    for i in m:
        s = re_br.sub('\n', i) # 将br转换为换行
        s = s.replace(' ', '') # 删除空格
        s = s.replace('=\\"', '') # 删除=\"
        s = s.replace('<\/', '')
        s = s.replace('\\">\\n', '\n') # 讲\">\n替换成换行
        num = s.find('运势学家王明磊')
        if num == 0:
            new_list.append(s)
    print(new_list[0])
    break
    s = filter_tags(req)
    print(s)
    break
    time.sleep(999)
    try:
        content = json.loads(text).get('data')
        cards = content.get('cards')  
        if (len(cards)>0):
            for j in range(len(cards)):
                card_type = cards[j].get('card_type')
                if (card_type == 9):
                    mblog = cards[j].get('mblog')
                    attitudes_count=mblog.get('attitudes_count')
                    comments_count=mblog.get('comments_count')
                    created_at=mblog.get('created_at')
                    reposts_count=mblog.get('reposts_count')
                    scheme=cards[j].get('scheme')
                    text1=mblog.get('text')
                    text2=filter_tags(text1)
                    print ( str(count) + "\n"+"发布时间："+str(created_at)+"\n"+"微博内容："+text2+"\n")
                    count = count + 1
            i = i + 1
            time.sleep(5)
        else:
            break 
    except Exception as e:
        print (e)
        pass

# https://weibo.com/u/7230522444?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=2#feedtop
