#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time           : 2025-12-20 16:52
@Author         : tao
@Python Version : 3.13.3
@Desc           : None

page 表需加索引： 
url : 用于判断页面是否已存在
domain_id + status + deep : 用于捞取待处理页面

"""
import time
from dao.common import SQLiteDB

PAGE_STATUS_PENDING = 0  # 待抓取
PAGE_STATUS_COMPLETED = 1  # 抓取完成

db = SQLiteDB("spider-common-db")

def GetPageByUrl(url):
    sql = f"""
    select * from page where url='{url}'
    """
    page = db.query_one(sql)
    return page

def GetPageCountByUrl(url):
    sql = f"""
    select count(*) num from page where url='{url}'
    """
    count_info = db.query_one(sql)
    return count_info['num']

def GetProcessingPages(count=10,domain_id=-1):
    sql = f"""
        -- 查询未完成的page
        select b.url,b.deep,a.max_deep,a.id as domain_id, b.id as page_id,a.sub_link_extract
        from domain a 
        left join page b on a.id=b.domain_id
        where b.status=0 and b.deep<=a.max_deep
        limit {count}
    """
    if domain_id != -1:
        sql = f"""
        -- 查询未完成的page
        select b.url,b.deep,a.max_deep,a.id as domain_id, b.id as page_id,a.sub_link_extract
        from domain a 
        left join page b on a.id=b.domain_id
        where b.status=0 and b.deep<=a.max_deep and a.id={domain_id}
        limit {count}
        """
        
    pages = db.query_all(sql)
    return pages


def InsertOneDomain(domain,deep,selector=""):
    now = int(time.time())
    insert_domain_sql = f"""
    INSERT INTO "domain" ("url", "max_deep", "sub_link_extract", "image_link_extract", "create_time", "update_time") VALUES ('{domain}', {deep}, '{selector}', NULL, {now}, {now});
    """
    ret = db.execute(insert_domain_sql)
    domain_id = ret.lastrowid

    insert_page_sql = f"""
        INSERT INTO "page" ("domain_id", "parent_id", "url", "data", "deep", "status", "create_time", "update_time") VALUES ({domain_id}, 0, '{domain}', NULL, 0, {PAGE_STATUS_PENDING}, {now}, {now});
    """
    ret = db.execute(insert_page_sql)
    print("执行成功，待抓取domain_id：", domain_id)
    return


def InsertPage(domain_id,parent_id,url,deep):
    # 先查询url是否存在
    if GetPageCountByUrl(url) > 0:
        print("页面已存在，跳过插入：", url)
        return
    now = int(time.time())
    insert_page_sql = f"""
    INSERT INTO "page" ("domain_id", "parent_id", "url", "data", "deep", "status", "create_time", "update_time") VALUES ({domain_id}, {parent_id}, '{url}', NULL, {deep}, {PAGE_STATUS_PENDING}, {now}, {now});
    """
    db.execute(insert_page_sql)
    return
    

def UpdatePage(page_id,title="",status=PAGE_STATUS_COMPLETED,data=""):
    now = int(time.time())
    update_sql = f"""
    UPDATE "page" SET "title"='{title}',"data"='{data}',"status"={status}, "update_time"={now} WHERE id={page_id};
    """
    db.execute(update_sql)
    return