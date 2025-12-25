#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time           : 2025-12-20 16:27
@Author         : tao
@Python Version : 3.13.3
@Desc           : None
"""
import tldextract
from urllib.parse import urljoin, urldefrag

def extract_main_domain(url: str) -> str | None:
    """
    提取主域名（registrable domain）
    示例：
    - https://www.a.b.example.com -> example.com
    - https://example.co.uk -> example.co.uk
    """
    if not url:
        return None
    ext = tldextract.extract(url)
    if not ext.domain or not ext.suffix:
        return None
    return f"{ext.domain}.{ext.suffix}"



def NormalizeUrl(base_url: str, href: str) -> str | None:
    """
    生成最终 URL，并去掉 #fragment（避免重复爬取）

    urljoin("https://example.com/docs/", "a.html")
    # https://example.com/docs/a.html
    """
    if not href:
        return None

    url = urljoin(base_url, href)
    url, _ = urldefrag(url)
    return url
