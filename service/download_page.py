#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time           : 2025-12-20 15:02
@Author         : tao
@Python Version : 3.13.3
@Desc           : 用于抓取web页面
"""

import sys
import os
import json
import time
import re

from bs4 import BeautifulSoup
import utils.tool_web_client as tool_web_client
import utils.tool_web as tool_web

from dao.page import GetProcessingPages,InsertPage,UpdatePage



def GetPageAndSubUrl(driver,url,sub_link_extract=""):
    """获取当前url的页面内容和子链接"""

    web_content,data_filepath = tool_web_client.get_web_with_catch_by_driver(False, driver, url)
    soup = BeautifulSoup(web_content, "html.parser")

    # 获取title
    title_text = soup.title.string if soup.title else None

    page_text = soup.get_text().strip()
    page_text_cleaned = re.sub(r'\n\s*\n+', '\n', page_text)
    print(page_text_cleaned)

    # 获取子链
    links = []
    if sub_link_extract == "":
        links = soup.find_all("a")
    else:
        # 可能有多个解析器
        sub_link_extract_list = json.loads(sub_link_extract)
        for selector in sub_link_extract_list:
            print("使用子链接解析器：", selector)
            elements = soup.select(selector)
            print("命中元素数量：", len(elements))
            for el in elements:
                if el.name == 'a':
                    links.append(el)
                else:
                    links.extend(el.find_all('a'))

    sub_link_set = set()
    for link in links:
        href_url = link.get("href")
        if not href_url: continue
        href_url = href_url.strip()
        # 生成最终url（有的url可能是相对路径）
        href_url = tool_web.NormalizeUrl(url, href_url)
        if not linkFilter(url, href_url):
            continue
        sub_link_set.add(href_url)

    return title_text, web_content, sub_link_set, data_filepath

def linkFilter(base_url,href_url):
    """
    过滤不需要的链接
    true: 保留
    false: 删除
    """
    if not href_url:
        return False
    if href_url.startswith("javascript:"):
        return False
    if href_url.startswith("#"):
        return False
    
    domain1 = tool_web.extract_main_domain(base_url)
    domain2 = tool_web.extract_main_domain(href_url)

    # 判断是否是当前主域名下的数据
    # TODO 需要进行配置化
    if domain1 != domain2:
        print("非主域名下网站", domain1, href_url)
        return False
    return True


def TaskDownloadPage(count=10,domain_id=-1):
    driver = tool_web_client.get_browser()
    # 1、捞取未抓取的页面和domain信息
    pages = GetProcessingPages(count,domain_id)
    # 2、获取页面信息，子链接，页面图片链接
    for page in pages:
        start_time = int(time.time())
        downloadOnePage(driver,page)
        end_time = int(time.time())
        print(f"页面下载耗时：{end_time - start_time} 秒")
    driver.quit()
    return

def downloadOnePage(driver,page_info):
    print("下载页面：",page_info)
    # 1 获取页面信息，子链接，页面图片链接
    url = page_info['url']
    sub_link_extract = page_info['sub_link_extract']

    title,web_content, sub_links,data_filepath = GetPageAndSubUrl(driver,url,sub_link_extract)
    print("子链接数量：",len(sub_links))

    # 2、数据存储：
    # 子链存储
    for link in sub_links:
        InsertPage(page_info['domain_id'], page_info['page_id'], link, page_info['deep'] + 1)
    
    # 图片存储

    # 状态更新
    UpdatePage(page_info['page_id'],title=title,data=data_filepath)
    return