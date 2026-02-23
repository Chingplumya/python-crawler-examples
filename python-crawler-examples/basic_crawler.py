#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python爬虫入门示例 - 基础网页爬取
作者：夕语
日期：2026-02-23
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

# ============== 基础配置 ==============
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# ============== 基础爬虫函数 ==============
def fetch_page(url, timeout=10):
    """
    获取网页内容
    
    Args:
        url: 目标网址
        timeout: 请求超时时间（秒）
    
    Returns:
        response对象，失败返回None
    """
    try:
        print(f"📡 正在请求：{url}")
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.encoding = response.apparent_encoding  # 自动识别编码
        print(f"✅ 请求成功，状态码：{response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{e}")
        return None

# ============== 解析函数 ==============
def parse_news_page(html):
    """
    解析新闻页面内容
    
    Args:
        html: 网页HTML内容
    
    Returns:
        包含新闻列表的字典
    """
    soup = BeautifulSoup(html, 'html.parser')
    news_list = []
    
    # 示例：查找所有新闻标题（根据实际网站结构调整选择器）
    # 这里使用通用的查找方式
    titles = soup.find_all(['h1', 'h2', 'h3'], class_=lambda x: x and ('title' in x.lower() or 'news' in x.lower()))
    
    for title in titles[:10]:  # 限制最多10条
        news_item = {
            'title': title.get_text(strip=True),
            'link': title.find('a')['href'] if title.find('a') else '',
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        news_list.append(news_item)
    
    return {'news': news_list, 'count': len(news_list)}

def parse_general_page(html):
    """
    通用页面解析 - 提取所有链接和文本
    
    Args:
        html: 网页HTML内容
    
    Returns:
        包含链接和文本的字典
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # 提取所有链接
    links = []
    for a in soup.find_all('a', href=True)[:20]:  # 限制最多20个
        links.append({
            'text': a.get_text(strip=True),
            'href': a['href']
        })
    
    # 提取所有段落文本
    paragraphs = []
    for p in soup.find_all('p')[:10]:  # 限制最多10段
        text = p.get_text(strip=True)
        if text:
            paragraphs.append(text)
    
    return {
        'links': links,
        'paragraphs': paragraphs,
        'title': soup.title.string if soup.title else 'No Title'
    }

# ============== 数据保存函数 ==============
def save_to_json(data, filename):
    """
    保存数据到JSON文件
    
    Args:
        data: 要保存的数据
        filename: 文件名
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 数据已保存到：{filename}")
    except Exception as e:
        print(f"❌ 保存失败：{e}")

def save_to_txt(data, filename):
    """
    保存数据到文本文件
    
    Args:
        data: 要保存的数据（字符串或列表）
        filename: 文件名
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            if isinstance(data, list):
                for item in data:
                    f.write(str(item) + '\n')
            else:
                f.write(str(data))
        print(f"💾 数据已保存到：{filename}")
    except Exception as e:
        print(f"❌ 保存失败：{e}")

# ============== 主爬虫函数 ==============
def crawl_website(url, parse_type='general', output_format='json'):
    """
    主爬虫函数
    
    Args:
        url: 目标网址
        parse_type: 解析类型 ('general' 或 'news')
        output_format: 输出格式 ('json' 或 'txt')
    
    Returns:
        爬取的数据
    """
    print("\n" + "="*50)
    print("🕷️  Python爬虫启动")
    print("="*50)
    
    # 获取网页
    response = fetch_page(url)
    if not response:
        return None
    
    # 解析内容
    print("\n🔍 正在解析页面内容...")
    if parse_type == 'news':
        data = parse_news_page(response.text)
    else:
        data = parse_general_page(response.text)
    
    print(f"✅ 解析完成，共获取 {data.get('count', len(data))} 条数据")
    
    # 保存数据
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if output_format == 'json':
        filename = f'crawl_result_{timestamp}.json'
        save_to_json(data, filename)
    else:
        filename = f'crawl_result_{timestamp}.txt'
        save_to_txt(data, filename)
    
    return data

# ============== 高级功能：带重试的爬虫 ==============
def crawl_with_retry(url, max_retries=3, delay=2):
    """
    带重试机制的爬虫
    
    Args:
        url: 目标网址
        max_retries: 最大重试次数
        delay: 重试间隔（秒）
    
    Returns:
        response对象
    """
    for i in range(max_retries):
        print(f"\n🔄 尝试请求 (第{i+1}/{max_retries}次)")
        response = fetch_page(url)
        if response and response.status_code == 200:
            return response
        if i < max_retries - 1:
            print(f"⏳ 等待{delay}秒后重试...")
            time.sleep(delay)
    return None

# ============== 示例用法 ==============
if __name__ == '__main__':
    # 示例1：爬取通用网页
    print("\n📋 示例1：爬取通用网页")
    test_url = 'https://www.python.org'
    result = crawl_website(test_url, parse_type='general', output_format='json')
    
    # 示例2：爬取新闻页面（需要实际新闻网站URL）
    # print("\n📋 示例2：爬取新闻页面")
    # news_url = 'https://example-news.com'
    # result = crawl_website(news_url, parse_type='news', output_format='json')
    
    # 示例3：带重试的爬取
    # print("\n📋 示例3：带重试的爬取")
    # response = crawl_with_retry(test_url, max_retries=3, delay=2)
    
    print("\n" + "="*50)
    print("✅ 爬虫执行完成")
    print("="*50)
