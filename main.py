#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time           : 2025-12-20 15:52
@Author         : tao
@Python Version : 3.13.3
@Desc           : None
"""
from service.download_page import GetPageAndSubUrl
from utils.tool_web_client  import get_browser

from dao.page import GetProcessingPages,InsertOneDomain
from service.download_page import TaskDownloadPage
import sys


def main():
    args = sys.argv[1:]
    print(args)
    if not args:
        print("参数错误")
        return
    process = args[0]
    if process == "":
        return
    elif process == "getOnePage":
        driver = get_browser()
        url = "https://bot.sannysoft.com"
        content,sub_links = GetPageAndSubUrl(driver,url)
        for i in sub_links:
            print(i)
        driver.quit()
    # elif process == "GetProcessingPages":
    #     GetProcessingPages()
    elif process == "InsertOneDomain": # 创建一个待抓取页面
        domain,deep,selector = args[1],int(args[2]),args[3]
        InsertOneDomain(domain,deep,selector)
    elif process == "TaskDownloadPage":
        count = int(args[1]) if len(args) > 1 else 10
        domain_id = int(args[2]) if len(args) > 2 else -1
        TaskDownloadPage(count, domain_id)
main()
