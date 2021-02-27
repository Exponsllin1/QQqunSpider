# -- coding: utf-8 --
# @Time : 2021/2/25 23:20
# @Author : Los Angeles Clippers
# @Email: 229456906@qq.com
# @sinaemail: angelesclippers@sina.com
import json
import re

import requests
import execjs
import pickle


class GetGroupList(object):

    def __init__(self):
        self.url = 'https://qun.qq.com/cgi-bin/qun_mgr/get_group_list'
        self.headers ={
            'origin': 'https://qun.qq.com',
            'pragma': 'no-cache',
            'referer': 'https://qun.qq.com/member.html',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
        }

    def rsgetcookie(self, cookie_name):
        f = open("cookied/{}_cookie.txt".format(cookie_name), encoding='utf-8')
        line = f.readlines()[0]
        f.close()
        ckl = re.findall(r'Cookie (.*?) ', line)
        cookies = {}
        for item in ckl[:]:
            s_item = item.split('=')
            cookies[s_item[0]] = s_item[1]
        print(cookies)
        return cookies

    def getbkn(self, skey):
        with open('lib/bkn.js', 'r') as f:
            js = f.read()
            f.close()
        com = execjs.compile(js)
        bkn = com.call('getbkn', skey)
        print(bkn)
        return bkn

    def get_gc(self, cookies, bkn):
        data = {
            'bkn': bkn
        }
        response = requests.post(self.url, headers=self.headers, data=data, cookies=cookies)
        jsdata = json.loads(response.text)
        print(jsdata)
        gc = re.findall(r"'gc': (.*?),", str(jsdata))
        gn = re.findall(r"'gn': '(.*?),", str(jsdata))
        print(gc)
        print(gn)
        print(len(gc), len(gn))
        return (gc, gn)

    def run(self, cookie, cookie_name):
        cookies = self.rsgetcookie(cookie_name=cookie_name)
        bkn = self.getbkn(cookies['skey'])
        gcgn = self.get_gc(cookies=cookies, bkn=bkn)
        return gcgn, bkn, cookies