# -- coding: utf-8 --
# @Time : 2021/2/25 21:56
# @Author : Los Angeles Clippers
# @Email: 229456906@qq.com
# @sinaemail: angelesclippers@sina.com

from cookieserverfunction.logincodeshow import LoginFuncRequests
from CrawlSpider.get_group_list import GetGroupList
from CrawlSpider.search_group_members import SearchGroupMembers


if __name__ == '__main__':
    logins = LoginFuncRequests()
    lck, cookie_name = logins.run()
    ggl = GetGroupList()
    gcgn, bkn, cookies = ggl.run(lck, cookie_name)
    sgm = SearchGroupMembers(gcgn, bkn, cookies)
    sgm.getMembers()

