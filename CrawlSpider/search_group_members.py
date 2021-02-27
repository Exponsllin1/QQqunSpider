# -- coding: utf-8 --
# @Time : 2021/2/25 23:41
# @Author : Los Angeles Clippers
# @Email: 229456906@qq.com
# @sinaemail: angelesclippers@sina.com

import requests
import json
import csv

class SearchGroupMembers(object):

    def __init__(self, gcgn, bkn, cookies):
        self.url = 'https://qun.qq.com/cgi-bin/qun_mgr/search_group_members'
        self.bkn = bkn
        self.gc = gcgn[0]
        self.gn = gcgn[1]
        self.cookies = cookies

        self.fp = open('datas/qq.csv', 'a', encoding='gb18030', newline='')
        self.fw = csv.writer(self.fp)

        self.fps = open('datas/qq_email.csv', 'a', encoding='gb18030', newline='')
        self.fws = csv.writer(self.fps)

        self.headers = {
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

    def getMembers(self):
        o = 0
        for gc, gn in zip(self.gc, self.gn):
            print(gn)
            i = 0
            for pg in range(0, 1000000, 21):
                data = {
                    'gc': gc,
                    'st': pg,
                    'end': 20 + pg,
                    'sort': '0',
                    'bkn': self.bkn,
                }
                response = requests.post(self.url, headers=self.headers, cookies=self.cookies, data=data)
                jsdata = json.loads(response.text)
                try:
                    mems = jsdata['mems']
                except KeyError as e:
                    break
                if len(mems) == 0:
                    break
                for item in mems:
                    i += 1
                    o += 1
                    qq = item['uin']
                    qq_email = str(qq) + '@qq.com'
                    nick = item['nick']
                    print(i, o, qq, nick)
                    # self.fw.writerow([qq, nick])
                    self.fws.writerow([str(qq), qq_email, nick])

        self.fp.close()
        self.fps.close()