#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态页面爬虫 - 模拟用户行为 + 数据爬取
作者：夕语
日期：2026-02-26

演示：
1. 打开网页后先模拟用户行为
2. 等待内容加载
3. 再爬取数据
"""

from playwright.sync_api import sync_playwright
import time
import random
import json
from datetime import datetime

# ============== 模拟人类行为函数 ==============

def human_like_scroll(page, times=3):
    """
    模拟人类滚动行为
    """
    print("📜 模拟滚动浏览...")
    for i in range(times):
        # 随机滚动距离
        scroll_distance = random.randint(300, 800)
        page.evaluate(f"window.scrollBy(0, {scroll_distance})")
        
        # 随机停顿（人类阅读时间）
        time.sleep(random.uniform(1.0, 2.5))
        
        print(f"  第{i+1}次滚动，停顿{random.uniform(1.0, 2.5):.1f}秒")
    
    # 滚动回顶部
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.5)

def human_like_mouse_move(page):
    """
    模拟鼠标移动
    """
    print("🖱️ 模拟鼠标移动...")
    for i in range(5):
        x = random.randint(100, 800)
        y = random.randint(100, 600)
        page.mouse.move(x, y)
        time.sleep(random.uniform(0.3, 0.8))

def human_like_clicks(page, selectors):
    """
    模拟点击行为（不提交表单）
    """
    print("👆 模拟点击交互...")
    for selector in selectors:
        try:
            element = page.query_selector(selector)
            if element:
                element.click()
                print(f"  点击了：{selector}")
                time.sleep(random.uniform(0.5, 1.5))
        except Exception as e:
            print(f"  点击失败 {selector}: {e}")

def random_delay(min_sec=1, max_sec=3):
    """
    随机延迟（模拟人类思考时间）
    """
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)
    return delay

# ============== 爬虫主函数 ==============

def crawl_with_behavior(url, crawl_config):
    """
    完整的爬虫流程：
    1. 打开网页
    2. 模拟用户行为
    3. 等待内容加载
    4. 爬取数据
    
    Args:
        url: 目标网址
        crawl_config: 爬取配置字典
            - simulate_behavior: 是否模拟行为
            - scroll_times: 滚动次数
            - wait_time: 额外等待时间
            - selectors: 要点击的元素
    """
    print("\n" + "="*60)
    print("🕷️  动态页面爬虫启动")
    print("="*60)
    
    with sync_playwright() as p:
        # 启动浏览器（建议先用有头模式调试）
        browser = p.chromium.launch(headless=True)
        
        # 创建上下文（设置更真实的指纹）
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-CN',
            timezone_id='Asia/Shanghai'
        )
        
        page = context.new_page()
        
        try:
            # ========== 步骤1：打开网页 ==========
            print(f"\n📡 步骤1：打开网页")
            print(f"   URL: {url}")
            page.goto(url, wait_until='networkidle', timeout=30000)
            print(f"   ✅ 页面加载完成")
            print(f"   标题：{page.title()}")
            
            # 初始等待
            time.sleep(2)
            
            # ========== 步骤2：模拟用户行为 ==========
            if crawl_config.get('simulate_behavior', True):
                print(f"\n🎭 步骤2：模拟用户行为")
                
                # 2.1 鼠标移动
                if crawl_config.get('mouse_move', True):
                    human_like_mouse_move(page)
                
                # 2.2 滚动浏览
                scroll_times = crawl_config.get('scroll_times', 3)
                human_like_scroll(page, times=scroll_times)
                
                # 2.3 模拟点击（可选）
                selectors = crawl_config.get('selectors', [])
                if selectors:
                    human_like_clicks(page, selectors)
                
                print(f"   ✅ 行为模拟完成")
            
            # ========== 步骤3：等待内容加载 ==========
            print(f"\n⏳ 步骤3：等待内容加载")
            
            # 额外等待时间
            extra_wait = crawl_config.get('wait_time', 2)
            delay = random_delay(1, extra_wait)
            print(f"   额外等待{delay:.1f}秒")
            
            # 等待特定元素（如果指定）
            wait_selector = crawl_config.get('wait_selector')
            if wait_selector:
                print(f"   等待元素：{wait_selector}")
                page.wait_for_selector(wait_selector, timeout=10000)
                print(f"   ✅ 目标元素已加载")
            
            # 截图保存（可选）
            if crawl_config.get('screenshot', False):
                screenshot_path = f'screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
                page.screenshot(path=screenshot_path)
                print(f"   📸 截图已保存：{screenshot_path}")
            
            # ========== 步骤4：爬取数据 ==========
            print(f"\n📊 步骤4：爬取数据")
            
            data = extract_data(page, crawl_config.get('extract_config', {}))
            
            # 保存数据
            if crawl_config.get('save_data', True):
                save_data(data)
            
            print(f"   ✅ 数据爬取完成")
            
            return data
            
        except Exception as e:
            print(f"\n❌ 爬取失败：{e}")
            return None
        finally:
            browser.close()
            print("\n🔒 浏览器已关闭")

# ============== 数据提取函数 ==============

def extract_data(page, config):
    """
    根据配置提取数据
    
    Args:
        page: Playwright页面对象
        config: 提取配置
            - title: 是否提取标题
            - links: 是否提取链接
            - text: 是否提取文本
            - custom_selectors: 自定义选择器
    """
    data = {
        'url': page.url,
        'title': page.title(),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # 提取链接
    if config.get('extract_links', True):
        links = page.query_selector_all('a')
        data['links'] = [
            {
                'text': link.inner_text()[:100],
                'href': link.get_attribute('href')
            }
            for link in links[:50]  # 限制数量
        ]
        print(f"   提取链接：{len(data['links'])} 条")
    
    # 提取文本
    if config.get('extract_text', True):
        paragraphs = page.query_selector_all('p')
        data['text'] = [
            p.inner_text()[:200]
            for p in paragraphs[:20]
            if p.inner_text().strip()
        ]
        print(f"   提取段落：{len(data['text'])} 段")
    
    # 自定义选择器
    custom_selectors = config.get('custom_selectors', {})
    for key, selector in custom_selectors.items():
        elements = page.query_selector_all(selector)
        data[key] = [el.inner_text() for el in elements]
        print(f"   提取{key}: {len(data[key])} 个")
    
    return data

def save_data(data):
    """
    保存数据到文件
    """
    filename = f'crawl_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"   💾 数据已保存：{filename}")

# ============== 特殊场景示例 ==============

def crawl_login_required_site(url, login_config, crawl_config):
    """
    爬取需要登录的网站
    
    流程：
    1. 打开登录页
    2. 填写表单
    3. 提交登录
    4. 等待跳转
    5. 模拟浏览
    6. 爬取数据
    """
    print("\n🔐 登录爬取模式启动")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 有头模式方便调试
        page = browser.new_page()
        
        try:
            # 1. 打开登录页
            page.goto(login_config['login_url'], wait_until='networkidle')
            
            # 2. 填写表单
            page.fill(login_config['username_selector'], login_config['username'])
            page.fill(login_config['password_selector'], login_config['password'])
            
            # 3. 模拟人类思考延迟
            time.sleep(random.uniform(1.0, 2.0))
            
            # 4. 点击登录
            page.click(login_config['submit_selector'])
            
            # 5. 等待跳转
            page.wait_for_url(crawl_config['target_url'], timeout=10000)
            print("✅ 登录成功")
            
            # 6. 模拟浏览
            human_like_scroll(page, times=3)
            
            # 7. 爬取数据
            data = extract_data(page, crawl_config.get('extract_config', {}))
            
            return data
            
        except Exception as e:
            print(f"❌ 登录爬取失败：{e}")
            return None
        finally:
            browser.close()

# ============== 示例用法 ==============

if __name__ == '__main__':
    # ========== 示例1：普通动态页面 ==========
    print("\n📋 示例1：普通动态页面爬取")
    
    config1 = {
        'simulate_behavior': True,  # 模拟用户行为
        'scroll_times': 3,           # 滚动3次
        'mouse_move': True,          # 鼠标移动
        'wait_time': 2,              # 额外等待2秒
        'screenshot': True,          # 保存截图
        'extract_config': {
            'extract_links': True,
            'extract_text': True,
        },
        'save_data': True
    }
    
    # 测试URL（替换为实际目标）
    test_url = 'https://news.ycombinator.com'
    # crawl_with_behavior(test_url, config1)
    
    # ========== 示例2：需要登录的网站 ==========
    print("\n📋 示例2：需要登录的网站")
    
    login_config = {
        'login_url': 'https://example.com/login',
        'username_selector': '#username',
        'password_selector': '#password',
        'submit_selector': '#submit-btn',
        'username': 'your_username',
        'password': 'your_password'
    }
    
    crawl_config = {
        'target_url': 'https://example.com/dashboard',
        'extract_config': {
            'extract_links': True,
            'extract_text': True,
        }
    }
    # crawl_login_required_site(test_url, login_config, crawl_config)
    
    # ========== 示例3：反爬严格的网站 ==========
    print("\n📋 示例3：反爬严格的网站")
    
    config3 = {
        'simulate_behavior': True,
        'scroll_times': 5,           # 更多滚动
        'mouse_move': True,
        'wait_time': 3,              # 更长等待
        'selectors': ['.nav-item', '.menu-link'],  # 模拟点击
        'screenshot': True,
        'extract_config': {
            'extract_links': True,
            'extract_text': True,
        },
        'save_data': True
    }
    # crawl_with_behavior('https://target-site.com', config3)
    
    print("\n" + "="*60)
    print("✅ 示例代码已准备就绪")
    print("="*60)
    print("\n💡 提示：取消注释对应的示例代码来运行")
