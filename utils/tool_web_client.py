#!/bin/env python3
# encoding=utf8
""" tools """
import time
import os
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils import tool_file
from bs4 import BeautifulSoup
import os
import csv
from selenium_stealth import stealth
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException


MAC_WEBDRIVER_PATH = r"/Users/th/Documents/workspace/spider-common/driver/chromedriver-mac-arm64/chromedriver"
chrome_binary_location = '/Users/th/Documents/workspace/spider-nga/driver/chrome-headless-shell-mac-arm64/chrome-headless-shell'  # 替换为实际的 Chrome 安装路径
# proxy = f"http://127.0.0.1:7890"

# 设定浏览器缓存目录
user_data_dir = "/tmp/chrome_cache"  # Linux/macOS
os.makedirs(user_data_dir, exist_ok=True)



def safe_execute_script(driver, script, *args):
    """安全执行 JS，自动处理意外弹出的 alert"""
    try:
        return driver.execute_script(script, *args)
    except UnexpectedAlertPresentException:
        # 处理 alert
        try:
            alert = driver.switch_to.alert
            print(f"⚠️ 检测到 alert，内容: '{alert.text}'，正在关闭...")
            alert.accept()  # 或 dismiss()
        except NoAlertPresentException:
            pass
        # 可选：重试一次（谨慎使用，避免死循环）
        try:
            return driver.execute_script(script, *args)
        except UnexpectedAlertPresentException:
            print("❌ 再次遇到 alert，放弃执行脚本")
            return None


PIC_DIR = "data_pics"
def get_web_with_catch_by_driver(day_change, driver, url):
    """ get_web_with_catch
    day_change : bool, 缓存是否需要天级变化
    func : functions
    """
    today = time.strftime("%Y%m%d", time.localtime())
    if day_change:
        catch_dir = f"cache/{today}/"
    else:
        catch_dir = f"cache/data/"

    domain = url.split("//")[1].split("/")[0]
    catch_dir = os.path.join(catch_dir, domain)
    if not os.path.exists(catch_dir):
        os.makedirs(catch_dir)

    cache_name = f"{url.split('//')[1].replace('/', '_')}.html"
    if len(cache_name) > 200:
        cache_name = tool_file.url_to_filename(cache_name)

    cache_filepath = os.path.join(catch_dir, cache_name)
    if os.path.exists(cache_filepath):
        with open(cache_filepath, "r", encoding="utf-8") as file:
            print("load_from_cache", url)
            return file.read(),cache_filepath
    print("load_from_web", url)
    driver.get(url)
    # 模拟下拉到最后

    # 执行 execute_script 前禁止弹窗

    count = 0
    last_height = safe_execute_script(driver,"return document.body.scrollHeight")

    while True:
        # 缓慢滚动：每次滚动一小段，直到接近底部
        scroll_pause_time = 0.2  # 每次滚动后暂停时间（秒）
        current_scroll = safe_execute_script(driver,"return window.pageYOffset;")
        target_scroll = safe_execute_script(driver,"return document.body.scrollHeight;")
        
        # 逐步滚动（例如每次滚动 1000 像素）
        while current_scroll < target_scroll:
            safe_execute_script(driver,"window.scrollBy(0,2000);")
            time.sleep(scroll_pause_time)
            current_scroll += 2000
            # 更新目标高度（因为可能在滚动中加载了新内容）
            target_scroll = safe_execute_script(driver,"return document.body.scrollHeight;")

        count += 1
        # time.sleep(1)  # 等待新内容充分加载

        # 检查是否到底（高度不再变化）
        new_height = safe_execute_script(driver,"return document.body.scrollHeight")
        if new_height == last_height:
            break

        if count >= 10:
            break

        last_height = new_height

    # 针对某些网站，增加随机等待时间，模拟人类行为
    sleep_time = random.uniform(2,3)
    print(f"Sleeping for {sleep_time:.2f} seconds to mimic human behavior...")
    time.sleep(sleep_time)

    web_content = driver.page_source
    if web_content:
        with open(cache_filepath, "w", encoding="utf-8") as file:
            file.write(web_content)
    

    return web_content,cache_filepath


def get_browser():
    service = Service(MAC_WEBDRIVER_PATH)
    chrome_options = webdriver.ChromeOptions()
    # 禁止加载图片
    prefs = {
        "profile.managed_default_content_settings.images": 2  # 2 表示禁用，1 表示启用
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument("--disable-web-security")  # 可选
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    # chrome_options.binary_location = chrome_binary_location
    # chrome_options.add_argument(f"--proxy-server={proxy}") # 设置代理
    browser = webdriver.Chrome(options=chrome_options, service=service)
    stealth(
        browser,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return browser


def download_image(driver,image_url):
    """ 
    download_image 
    添加缓存判断功能，如果文件已存在则跳过下载
    """
    import requests
    # 网络图片 https://img.haijiaoluv.top/cdn/1/3681040.webp 文件存储路径：img.haijiaoluv.top/3681040.webp
    save_path = image_url.split("//")[1]  # 去掉协议部分
    save_path_list = save_path.split('/')  # 去掉多余的路径部分
    save_path = save_path_list[0] + '/' + save_path_list[-1]
    save_path = os.path.join(PIC_DIR, save_path)
    if not os.path.exists(os.path.dirname(save_path)):
        os.makedirs(os.path.dirname(save_path))

    if os.path.exists(save_path):
        print(f"Image already exists at {save_path}, skipping download.")
        return

    # 通过driver下载图片，避免反爬虫
    # 图片中可能存在gif图，需要保存为webp格式
    try:
        driver.get(image_url)
        image_data = driver.find_element("tag name", "img").screenshot_as_png
        with open(save_path, "wb") as f:
            f.write(image_data)
        print(f"Image downloaded and saved to {save_path}")
    except Exception as e:
        print(f"Failed to download image from {image_url}. Error: {e}")
    