#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬虫数据入库系统 - 实战项目
作者：夕语
日期：2026-02-26

功能：
1. 爬取网页数据
2. 自动存储到MySQL数据库
3. 去重处理
4. 数据查询和导出
"""

import mysql.connector
from mysql.connector import Error
import requests
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime
import json

# ============== 数据库管理类 ==============

class DatabaseManager:
    """数据库管理类"""
    
    def __init__(self, config):
        """
        初始化数据库连接
        
        Args:
            config: 数据库配置字典
                - host: 主机名
                - database: 数据库名
                - user: 用户名
                - password: 密码
        """
        self.config = config
        self.connection = None
        self.connect()
    
    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            print(f"✅ 数据库连接成功：{self.config['database']}")
        except Error as e:
            print(f"❌ 数据库连接失败：{e}")
            raise
    
    def create_tables(self):
        """创建必要的表"""
        cursor = self.connection.cursor()
        
        # 爬虫数据表
        create_crawler_table = """
        CREATE TABLE IF NOT EXISTS crawler_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url_hash VARCHAR(64) UNIQUE NOT NULL,
            title VARCHAR(500),
            url VARCHAR(1000),
            content TEXT,
            source VARCHAR(100),
            crawl_time DATETIME,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_url_hash (url_hash),
            INDEX idx_crawl_time (crawl_time),
            INDEX idx_source (source)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        
        # 爬取日志表
        create_log_table = """
        CREATE TABLE IF NOT EXISTS crawl_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(1000),
            status_code INT,
            error_message TEXT,
            crawl_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_status (status_code),
            INDEX idx_crawl_time (crawl_time)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        
        try:
            cursor.execute(create_crawler_table)
            cursor.execute(create_log_table)
            self.connection.commit()
            print("✅ 表创建成功")
        except Error as e:
            print(f"❌ 创建表失败：{e}")
            self.connection.rollback()
        finally:
            cursor.close()
    
    def url_to_hash(self, url):
        """
        将URL转换为MD5哈希值（用于去重）
        
        Args:
            url: 网址
        
        Returns:
            MD5哈希字符串
        """
        return hashlib.md5(url.encode('utf-8')).hexdigest()
    
    def is_duplicate(self, url):
        """
        检查URL是否已存在
        
        Args:
            url: 网址
        
        Returns:
            True=重复，False=不重复
        """
        url_hash = self.url_to_hash(url)
        cursor = self.connection.cursor()
        
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM crawler_data WHERE url_hash = %s",
                (url_hash,)
            )
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            print(f"❌ 检查重复失败：{e}")
            return False
        finally:
            cursor.close()
    
    def save_crawl_data(self, data):
        """
        保存爬取数据
        
        Args:
            data: 数据字典
                - url: 网址
                - title: 标题
                - content: 内容
                - source: 来源
                - crawl_time: 爬取时间
        
        Returns:
            插入的ID，失败返回None
        """
        url_hash = self.url_to_hash(data['url'])
        
        # 检查是否重复
        if self.is_duplicate(data['url']):
            print(f"⚠️  跳过重复URL：{data['url'][:50]}...")
            return None
        
        cursor = self.connection.cursor()
        
        insert_query = """
        INSERT INTO crawler_data (url_hash, url, title, content, source, crawl_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        values = (
            url_hash,
            data['url'],
            data.get('title', ''),
            data.get('content', ''),
            data.get('source', ''),
            data.get('crawl_time', datetime.now())
        )
        
        try:
            cursor.execute(insert_query, values)
            self.connection.commit()
            print(f"✅ 数据保存成功，ID: {cursor.lastrowid}")
            return cursor.lastrowid
        except Error as e:
            print(f"❌ 保存数据失败：{e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()
    
    def log_error(self, url, status_code, error_message):
        """
        记录爬取错误日志
        
        Args:
            url: 网址
            status_code: HTTP状态码
            error_message: 错误信息
        """
        cursor = self.connection.cursor()
        
        insert_query = """
        INSERT INTO crawl_logs (url, status_code, error_message)
        VALUES (%s, %s, %s)
        """
        
        values = (url, status_code, error_message)
        
        try:
            cursor.execute(insert_query, values)
            self.connection.commit()
        except Error as e:
            print(f"❌ 记录日志失败：{e}")
            self.connection.rollback()
        finally:
            cursor.close()
    
    def query_data(self, conditions=None, limit=100):
        """
        查询数据
        
        Args:
            conditions: 查询条件字典
                - source: 来源
                - start_date: 开始日期
                - end_date: 结束日期
            limit: 返回数量限制
        
        Returns:
            查询结果列表
        """
        cursor = self.connection.cursor()
        
        query = "SELECT * FROM crawler_data WHERE 1=1"
        params = []
        
        if conditions:
            if 'source' in conditions:
                query += " AND source = %s"
                params.append(conditions['source'])
            
            if 'start_date' in conditions:
                query += " AND crawl_time >= %s"
                params.append(conditions['start_date'])
            
            if 'end_date' in conditions:
                query += " AND crawl_time <= %s"
                params.append(conditions['end_date'])
        
        query += " ORDER BY crawl_time DESC LIMIT %s"
        params.append(limit)
        
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"❌ 查询失败：{e}")
            return []
        finally:
            cursor.close()
    
    def export_to_json(self, filename, conditions=None, limit=1000):
        """
        导出数据到JSON文件
        
        Args:
            filename: 输出文件名
            conditions: 查询条件
            limit: 数量限制
        """
        data = self.query_data(conditions, limit)
        
        # 转换为字典列表
        columns = ['id', 'url_hash', 'title', 'url', 'content', 'source', 'crawl_time']
        result = []
        for row in data:
            row_dict = dict(zip(columns, row))
            result.append(row_dict)
        
        # 保存到文件
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 已导出 {len(result)} 条数据到：{filename}")
    
    def get_statistics(self):
        """
        获取统计信息
        
        Returns:
            统计信息字典
        """
        cursor = self.connection.cursor()
        
        stats = {}
        
        # 总数据量
        cursor.execute("SELECT COUNT(*) FROM crawler_data")
        stats['total_count'] = cursor.fetchone()[0]
        
        # 按来源统计
        cursor.execute("""
            SELECT source, COUNT(*) as count 
            FROM crawler_data 
            GROUP BY source 
            ORDER BY count DESC
        """)
        stats['by_source'] = cursor.fetchall()
        
        # 最近爬取时间
        cursor.execute("SELECT MAX(crawl_time) FROM crawler_data")
        stats['last_crawl'] = cursor.fetchone()[0]
        
        cursor.close()
        return stats
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("🔒 数据库连接已关闭")

# ============== 爬虫类 ==============

class CrawlerWithDB:
    """带数据库存储的爬虫"""
    
    def __init__(self, db_config):
        """
        初始化爬虫
        
        Args:
            db_config: 数据库配置
        """
        self.db = DatabaseManager(db_config)
        self.db.create_tables()
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_page(self, url, timeout=10):
        """
        获取网页内容
        
        Args:
            url: 网址
            timeout: 超时时间
        
        Returns:
            HTML内容，失败返回None
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=timeout)
            response.encoding = response.apparent_encoding
            return response.text
        except Exception as e:
            print(f"❌ 请求失败 {url}: {e}")
            self.db.log_error(url, 0, str(e))
            return None
    
    def parse_page(self, url, html):
        """
        解析网页内容
        
        Args:
            url: 网址
            html: HTML内容
        
        Returns:
            数据字典
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取标题
        title = soup.title.string if soup.title else ''
        
        # 提取所有段落文本
        paragraphs = soup.find_all('p')
        content = '\n'.join([p.get_text(strip=True) for p in paragraphs])
        
        # 提取来源（从域名）
        from urllib.parse import urlparse
        source = urlparse(url).netloc
        
        return {
            'url': url,
            'title': title[:500] if title else '',
            'content': content[:10000],  # 限制长度
            'source': source,
            'crawl_time': datetime.now()
        }
    
    def crawl_and_save(self, url):
        """
        爬取并保存到数据库
        
        Args:
            url: 网址
        
        Returns:
            保存的ID，失败返回None
        """
        print(f"\n🕷️  开始爬取：{url}")
        
        # 检查是否重复
        if self.db.is_duplicate(url):
            print(f"⚠️  URL已存在，跳过")
            return None
        
        # 获取网页
        html = self.fetch_page(url)
        if not html:
            return None
        
        # 解析内容
        data = self.parse_page(url, html)
        
        # 保存到数据库
        saved_id = self.db.save_crawl_data(data)
        
        return saved_id
    
    def crawl_batch(self, url_list):
        """
        批量爬取
        
        Args:
            url_list: URL列表
        
        Returns:
            成功数量
        """
        print(f"\n📋 开始批量爬取，共 {len(url_list)} 个URL")
        
        success_count = 0
        for i, url in enumerate(url_list, 1):
            print(f"\n[{i}/{len(url_list)}]")
            result = self.crawl_and_save(url)
            if result:
                success_count += 1
        
        print(f"\n✅ 批量爬取完成，成功：{success_count}/{len(url_list)}")
        return success_count
    
    def show_stats(self):
        """显示统计信息"""
        stats = self.db.get_statistics()
        
        print("\n" + "="*40)
        print("📊 数据库统计")
        print("="*40)
        print(f"总数据量：{stats['total_count']}")
        print(f"最后爬取：{stats['last_crawl']}")
        print("\n按来源统计:")
        for source, count in stats['by_source']:
            print(f"  {source}: {count}")
        print("="*40)
    
    def close(self):
        """关闭连接"""
        self.db.close()

# ============== 示例用法 ==============

if __name__ == '__main__':
    # ========== 数据库配置 ==========
    DB_CONFIG = {
        'host': 'localhost',
        'database': 'crawler_db',
        'user': 'root',
        'password': 'your_password'  # 替换为你的密码
    }
    
    print("\n" + "="*60)
    print("🕷️  爬虫数据入库系统")
    print("="*60)
    
    # ========== 创建爬虫实例 ==========
    # crawler = CrawlerWithDB(DB_CONFIG)
    
    # ========== 单个URL爬取 ==========
    # test_urls = [
    #     'https://www.python.org',
    #     'https://github.com',
    #     'https://stackoverflow.com',
    # ]
    # for url in test_urls:
    #     crawler.crawl_and_save(url)
    
    # ========== 批量爬取 ==========
    # url_list = [
    #     'https://news.ycombinator.com',
    #     'https://www.reddit.com/r/Python',
    #     'https://medium.com/topic/python',
    # ]
    # crawler.crawl_batch(url_list)
    
    # ========== 查询数据 ==========
    # results = crawler.db.query_data(
    #     conditions={'source': 'www.python.org'},
    #     limit=10
    # )
    # for row in results:
    #     print(row)
    
    # ========== 导出数据 ==========
    # crawler.db.export_to_json('exported_data.json', limit=100)
    
    # ========== 显示统计 ==========
    # crawler.show_stats()
    
    # ========== 关闭连接 ==========
    # crawler.close()
    
    print("\n⚠️  演示模式（需要真实数据库请取消注释代码）")
    print("\n💡 下一步：")
    print("1. 安装MySQL并创建数据库")
    print("2. 修改DB_CONFIG配置")
    print("3. 运行示例代码")
    print("4. 查看数据库中的数据")
