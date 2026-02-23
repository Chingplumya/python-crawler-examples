#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python爬虫进阶示例 - 浏览器自动化（Playwright）
作者：夕语
日期：2026-02-23

适用于需要执行JavaScript的动态网站
"""

from playwright.sync_api import sync_playwright
import json
import time
from datetime import datetime

# ============== 基础浏览器爬虫 ==============
def crawl_with_browser(url, headless=True):
    """
    使用浏览器爬取动态网页
    
    Args:
        url: 目标网址
        headless: 是否无头模式（不显示浏览器窗口）
    
    Returns:
        页面内容字典
    """
    print("\n🌐 启动浏览器...")
    
    with sync_playwright() as p:
        # 启动浏览器（支持 chromium, firefox, webkit）
        browser = p.chromium.launch(headless=headless)
        
        # 创建新页面
        page = browser.new_page(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        try:
            print(f"📡 正在访问：{url}")
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # 等待页面加载完成
            time.sleep(2)
            
            # 获取页面信息
            result = {
                'title': page.title(),
                'url': page.url,
                'content': page.content()[:5000],  # 限制长度
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"✅ 页面加载成功：{result['title']}")
            
            # 提取所有链接
            links = page.query_selector_all('a')
            result['links_count'] = len(links)
            result['sample_links'] = [
                {
                    'text': link.inner_text()[:50],
                    'href': link.get_attribute('href')
                }
                for link in links[:20]
            ]
            
            return result
            
        except Exception as e:
            print(f"❌ 爬取失败：{e}")
            return None
        finally:
            browser.close()
            print("🔒 浏览器已关闭")

# ============== 模拟用户行为 ==============
def simulate_user_interaction(url, search_keyword=None):
    """
    模拟用户交互行为（点击、输入等）
    
    Args:
        url: 目标网址
        search_keyword: 搜索关键词（如果需要搜索）
    
    Returns:
        操作结果
    """
    print("\n🎭 模拟用户交互...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 显示浏览器窗口
        page = browser.new_page()
        
        try:
            page.goto(url, wait_until='networkidle')
            
            # 如果有搜索关键词，执行搜索
            if search_keyword:
                print(f"🔍 搜索关键词：{search_keyword}")
                
                # 查找搜索框（需要根据实际网站调整选择器）
                search_box = page.query_selector('input[type="search"], input[name="q"], input[placeholder*="搜索"]')
                
                if search_box:
                    search_box.fill(search_keyword)
                    search_box.press('Enter')
                    page.wait_for_load_state('networkidle')
                    print("✅ 搜索完成")
                else:
                    print("⚠️ 未找到搜索框")
            
            # 截图保存
            screenshot_path = f'screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            page.screenshot(path=screenshot_path)
            print(f"📸 截图已保存：{screenshot_path}")
            
            # 获取当前页面内容
            result = {
                'title': page.title(),
                'url': page.url,
                'screenshot': screenshot_path,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return result
            
        except Exception as e:
            print(f"❌ 操作失败：{e}")
            return None
        finally:
            browser.close()

# ============== 处理滚动加载 ==============
def crawl_infinite_scroll(url, scroll_times=3):
    """
    爬取无限滚动加载的页面
    
    Args:
        url: 目标网址
        scroll_times: 滚动次数
    
    Returns:
        页面内容
    """
    print("\n📜 处理无限滚动页面...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, wait_until='networkidle')
            
            # 多次滚动以加载更多内容
            for i in range(scroll_times):
                print(f"🔄 第{i+1}次滚动...")
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(2)  # 等待内容加载
            
            # 滚动回顶部
            page.evaluate('window.scrollTo(0, 0)')
            
            # 获取全部内容
            content = page.content()
            
            print(f"✅ 滚动完成，页面长度：{len(content)}")
            
            return {
                'url': url,
                'content_length': len(content),
                'scroll_times': scroll_times,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            print(f"❌ 爬取失败：{e}")
            return None
        finally:
            browser.close()

# ============== 反爬策略处理 ==============
def crawl_with_anti_detection(url):
    """
    带反检测的爬虫
    
    Returns:
        页面内容
    """
    print("\n🥷 使用反检测模式...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        
        # 创建上下文，设置更真实的浏览器指纹
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-CN',
            timezone_id='Asia/Shanghai'
        )
        
        # 隐藏自动化特征
        page = context.new_page()
        page.add_init_script('''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        ''')
        
        try:
            page.goto(url, wait_until='networkidle')
            
            result = {
                'title': page.title(),
                'url': page.url,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"✅ 爬取成功：{result['title']}")
            return result
            
        except Exception as e:
            print(f"❌ 爬取失败：{e}")
            return None
        finally:
            context.close()
            browser.close()

# ============== 示例用法 ==============
if __name__ == '__main__':
    # 示例1：基础浏览器爬取
    print("\n📋 示例1：基础浏览器爬取")
    test_url = 'https://www.python.org'
    result = crawl_with_browser(test_url, headless=True)
    if result:
        print(f"页面标题：{result['title']}")
        print(f"链接数量：{result['links_count']}")
    
    # 示例2：模拟用户交互（需要时取消注释）
    # print("\n📋 示例2：模拟用户交互")
    # result = simulate_user_interaction('https://www.bing.com', search_keyword='Python爬虫')
    
    # 示例3：处理无限滚动
    # print("\n📋 示例3：处理无限滚动")
    # result = crawl_infinite_scroll('https://news.ycombinator.com', scroll_times=3)
    
    # 示例4：反检测模式
    # print("\n📋 示例4：反检测模式")
    # result = crawl_with_anti_detection('https://www.example.com')
    
    print("\n" + "="*50)
    print("✅ 所有示例执行完成")
    print("="*50)
