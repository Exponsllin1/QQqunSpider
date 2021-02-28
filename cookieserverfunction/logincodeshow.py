# -- coding: utf-8 --
# @Time : 2021/2/25 20:25
# @Author : Los Angeles Clippers
# @Email: 229456906@qq.com
# @sinaemail: angelesclippers@sina.com
import pickle
import re
import time

import execjs
import requests
from PIL import Image
import matplotlib.pyplot as plt

from common import utils


class LoginFuncRequests(object):
    def __init__(self):
        self.session = requests.session()
        self.img_path = 'cookieserverfunction/image/code.png'

    def code_show(self):
        url = 'https://ssl.ptlogin2.qq.com/ptqrshow?'
        data = {
            'appid': '715030901',
            'e': '2',
            'l': 'M',
            's': '3',
            'd': '72',
            'v': '4',
            't': '0.9292435301685353',
            'daid': '73',
            'pt_3rd_aid': '0',
        }
        utils.headers['Host'] = 'ssl.ptlogin2.qq.com'
        utils.headers['Referer'] = 'https://xui.ptlogin2.qq.com/'
        print(utils.headers)
        response = self.session.get(url, params=data, headers=utils.headers)
        utils.headers.pop('Host')
        print(response.status_code)
        with open('cookieserverfunction/image/code.png', 'wb') as f:
            f.write(response.content)
            f.close()
        print(response.cookies)
        return response.cookies

    def get_ptqrtoken(self, cookies):
        with open('common/bkn.js', 'r') as f:
            js = f.read()
            f.close()
        com = execjs.compile(js)
        ptqrtoken = com.call('ptqrtoken', re.search(r'qrsig=(.*?) ', str(cookies)).group(1))
        print('ptqrtoken:', ptqrtoken)
        return ptqrtoken

    def pt_login_sig(self):
        url = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?'
        data = {
            'pt_disable_pwd': '1',
            'appid': '715030901',
            'daid': '73',
            'pt_no_auth': '1',
            's_url': 'https://qun.qq.com/',
        }
        print(utils.headers)
        utils.headers['referer'] = 'https://qun.qq.com/'
        response = self.session.get(url, params=data, headers=utils.headers)
        print(response.cookies)
        login_sig = re.search(r'pt_login_sig=(.*?) ', str(response.cookies)).group(1)
        print('login_sig:', login_sig)
        return login_sig, response.cookies

    def check_Codeshow(self, ptqrtoken, login_sig, ck):
        url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?'
        action = int(time.time() * 1000)
        data = {
            'u1': 'https://qun.qq.com/',
            'ptqrtoken': ptqrtoken,
            'ptredirect': '1',
            'h': '1',
            't': '1',
            'g': '1',
            'from_ui': '1',
            'ptlang': '2052',
            'action': '0-0-' + str(action),
            'js_ver': '21020514',
            'js_type': '1',
            'login_sig': login_sig,
            'pt_uistyle': '40',
            'aid': '715030901',
            'daid': '73',
        }
        utils.headers['referer'] = 'https://xui.ptlogin2.qq.com/'
        response = self.session.get(url, params=data, headers=utils.headers, cookies=ck)
        print(response.text)
        return response.text

    def showc(self, ptqrtoken, login_sig, ck):
        # 显示二维码
        img = Image.open(self.img_path)  # 打开图片，返回PIL image对象
        plt.figure("请使用app扫描验证码", figsize=(5, 4))
        plt.ion()  # 打开交互模式
        plt.axis('off')  # 不需要坐标轴
        plt.imshow(img)
        global pausing
        pausing = True
        while pausing:
            plt.pause(0.05)
            while True:
                bg = self.check_Codeshow(ptqrtoken, login_sig, ck)
                if '登录成功' in str(bg):
                    pausing = False
                    ebg = 1
                    break
                if '二维码认证中' in str(bg):
                    pass
                if '二维码已失效' in str(bg):
                    pausing = False
                    ebg = 0
                    break
                if '本次登录已被拒绝' in str(bg):
                    pausing = False
                    ebg = 0
                    break
                time.sleep(1)
        plt.ioff()  # 显示完后一定要配合使用plt.ioff()关闭交互模式，否则可能出奇怪的问题
        plt.clf()  # 清空图片
        plt.close()  # 清空窗口
        return ebg, bg

    def get_cookie(self, url):
        utils.headers['referer'] = 'https://xui.ptlogin2.qq.com/'
        response = self.session.get(url, headers=utils.headers, allow_redirects=False)
        print(response.cookies)
        return response.cookies

    def run(self):
        cookies = self.code_show()
        ptqrtoken = self.get_ptqrtoken(cookies=cookies)
        login_sig, ck = self.pt_login_sig()
        ebg, bg = self.showc(ptqrtoken, login_sig, ck)
        if ebg == 0:
            self.run()
        else:
            url = re.search(r"ptuiCB\('0','0','(.*?)'", bg).group(1)
            # print(url)
            lck = self.get_cookie(url=url)
            cookie_name = re.search(r'uin=(.*?)&', bg).group(1)
            with open("cookied/{}_cookie.txt".format(cookie_name), 'w') as f:
                f.write(str(lck))
            return lck, cookie_name