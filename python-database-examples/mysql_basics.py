#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库学习示例1 - MySQL基础操作
作者：夕语
日期：2026-02-26

涵盖：
1. 数据库连接
2. 创建表和数据库
3. CRUD操作（增删改查）
4. 事务处理
5. 索引优化
"""

import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime

# ============== 数据库连接 ==============

def create_connection(host_name, db_name, user_name, user_password):
    """
    创建MySQL数据库连接
    
    Args:
        host_name: 主机名（本地：localhost）
        db_name: 数据库名
        user_name: 用户名
        user_password: 密码
    
    Returns:
        connection对象
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print(f"✅ 成功连接到数据库 '{db_name}'")
    except Error as e:
        print(f"❌ 连接失败：{e}")
    
    return connection

def create_database(host_name, user_name, user_password, db_name):
    """
    创建新数据库
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"✅ 数据库 '{db_name}' 创建成功")
    except Error as e:
        print(f"❌ 创建数据库失败：{e}")
    finally:
        if connection:
            connection.close()

# ============== 创建表 ==============

def create_table(connection, create_table_query):
    """
    创建数据表
    
    Args:
        connection: 数据库连接
        create_table_query: CREATE TABLE语句
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("✅ 表创建成功")
    except Error as e:
        print(f"❌ 创建表失败：{e}")

# ============== CRUD操作 ==============

def insert_data(connection, query, data=None):
    """
    插入数据
    
    Args:
        connection: 数据库连接
        query: INSERT语句
        data: 数据元组
    """
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print(f"✅ 插入成功，影响行数：{cursor.rowcount}")
        return cursor.lastrowid  # 返回最后插入的ID
    except Error as e:
        print(f"❌ 插入失败：{e}")
        return None

def insert_many(connection, query, data_list):
    """
    批量插入数据
    
    Args:
        connection: 数据库连接
        query: INSERT语句
        data_list: 数据列表
    """
    cursor = connection.cursor()
    try:
        cursor.executemany(query, data_list)
        connection.commit()
        print(f"✅ 批量插入成功，影响行数：{cursor.rowcount}")
        return cursor.rowcount
    except Error as e:
        print(f"❌ 批量插入失败：{e}")
        return 0

def select_query(connection, query):
    """
    查询数据
    
    Args:
        connection: 数据库连接
        query: SELECT语句
    
    Returns:
        查询结果列表
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"❌ 查询失败：{e}")
        return []

def update_data(connection, query, data=None):
    """
    更新数据
    
    Args:
        connection: 数据库连接
        query: UPDATE语句
        data: 数据元组
    """
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print(f"✅ 更新成功，影响行数：{cursor.rowcount}")
        return cursor.rowcount
    except Error as e:
        print(f"❌ 更新失败：{e}")
        return 0

def delete_data(connection, query, data=None):
    """
    删除数据
    
    Args:
        connection: 数据库连接
        query: DELETE语句
        data: 数据元组
    """
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print(f"✅ 删除成功，影响行数：{cursor.rowcount}")
        return cursor.rowcount
    except Error as e:
        print(f"❌ 删除失败：{e}")
        return 0

# ============== 事务处理 ==============

def execute_transaction(connection, queries):
    """
    执行事务（多个操作要么全部成功，要么全部失败）
    
    Args:
        connection: 数据库连接
        queries: SQL语句列表
    """
    cursor = connection.cursor()
    try:
        for query in queries:
            cursor.execute(query)
        connection.commit()
        print("✅ 事务执行成功")
        return True
    except Error as e:
        connection.rollback()  # 回滚
        print(f"❌ 事务失败，已回滚：{e}")
        return False

# ============== 索引操作 ==============

def create_index(connection, index_name, table_name, column_name):
    """
    创建索引
    
    Args:
        connection: 数据库连接
        index_name: 索引名
        table_name: 表名
        column_name: 列名
    """
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE INDEX {index_name} ON {table_name}({column_name})")
        connection.commit()
        print(f"✅ 索引 '{index_name}' 创建成功")
    except Error as e:
        print(f"❌ 创建索引失败：{e}")

def show_indexes(connection, table_name):
    """
    查看表的索引
    
    Args:
        connection: 数据库连接
        table_name: 表名
    """
    cursor = connection.cursor()
    try:
        cursor.execute(f"SHOW INDEX FROM {table_name}")
        indexes = cursor.fetchall()
        print(f"\n📊 表 '{table_name}' 的索引:")
        for idx in indexes:
            print(f"  - {idx[2]} ({idx[4]})")  # 索引名，列名
        return indexes
    except Error as e:
        print(f"❌ 查看索引失败：{e}")
        return []

# ============== 示例用法 ==============

if __name__ == '__main__':
    # ========== 配置 ==========
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'your_password',  # 替换为你的密码
        'database': 'crawler_db'
    }
    
    print("\n" + "="*60)
    print("📚 MySQL基础操作示例")
    print("="*60)
    
    # ========== 步骤1：创建数据库 ==========
    print("\n📋 步骤1：创建数据库")
    # create_database('localhost', 'root', 'your_password', 'crawler_db')
    
    # ========== 步骤2：连接数据库 ==========
    print("\n📋 步骤2：连接数据库")
    # connection = create_connection(
    #     DB_CONFIG['host'],
    #     DB_CONFIG['database'],
    #     DB_CONFIG['user'],
    #     DB_CONFIG['password']
    # )
    
    # 如果没有真实数据库，用模拟连接演示
    connection = None
    print("⚠️  演示模式（需要真实数据库请取消注释上面的代码）")
    
    # ========== 步骤3：创建表 ==========
    print("\n📋 步骤3：创建表")
    
    create_crawler_data_table = """
    CREATE TABLE IF NOT EXISTS crawler_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(500) NOT NULL,
        url VARCHAR(1000),
        content TEXT,
        source VARCHAR(100),
        crawl_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_title (title),
        INDEX idx_crawl_time (crawl_time)
    )
    """
    # create_table(connection, create_crawler_data_table)
    
    # ========== 步骤4：插入数据 ==========
    print("\n📋 步骤4：插入数据")
    
    # 单条插入
    insert_query = """
    INSERT INTO crawler_data (title, url, content, source)
    VALUES (%s, %s, %s, %s)
    """
    # data = ("示例文章标题", "https://example.com/article1", "文章内容...", "Example Site")
    # insert_data(connection, insert_query, data)
    
    # 批量插入
    # data_list = [
    #     ("文章1", "https://example.com/1", "内容1", "Site1"),
    #     ("文章2", "https://example.com/2", "内容2", "Site2"),
    #     ("文章3", "https://example.com/3", "内容3", "Site3"),
    # ]
    # insert_many(connection, insert_query, data_list)
    
    # ========== 步骤5：查询数据 ==========
    print("\n📋 步骤5：查询数据")
    
    # 查询所有
    # select_all = "SELECT * FROM crawler_data"
    # results = select_query(connection, select_all)
    # for row in results:
    #     print(row)
    
    # 条件查询
    # select_where = "SELECT * FROM crawler_data WHERE source = %s"
    # results = select_query(connection, select_where, ("Site1",))
    
    # 排序查询
    # select_order = "SELECT * FROM crawler_data ORDER BY crawl_time DESC LIMIT 10"
    # results = select_query(connection, select_order)
    
    # ========== 步骤6：更新数据 ==========
    print("\n📋 步骤6：更新数据")
    
    # update_query = """
    # UPDATE crawler_data
    # SET content = %s
    # WHERE id = %s
    # """
    # update_data(connection, update_query, ("更新后的内容", 1))
    
    # ========== 步骤7：删除数据 ==========
    print("\n📋 步骤7：删除数据")
    
    # delete_query = "DELETE FROM crawler_data WHERE id = %s"
    # delete_data(connection, delete_query, (1,))
    
    # ========== 步骤8：事务处理 ==========
    print("\n📋 步骤8：事务处理")
    
    # transaction_queries = [
    #     "INSERT INTO crawler_data (title, url) VALUES ('事务测试1', 'https://test.com/1')",
    #     "INSERT INTO crawler_data (title, url) VALUES ('事务测试2', 'https://test.com/2')",
    #     "UPDATE crawler_data SET content = '批量更新' WHERE id > 0",
    # ]
    # execute_transaction(connection, transaction_queries)
    
    # ========== 步骤9：索引优化 ==========
    print("\n📋 步骤9：索引优化")
    
    # create_index(connection, 'idx_source', 'crawler_data', 'source')
    # show_indexes(connection, 'crawler_data')
    
    # ========== 步骤10：关闭连接 ==========
    if connection:
        connection.close()
        print("\n🔒 数据库连接已关闭")
    
    print("\n" + "="*60)
    print("✅ 示例代码已准备就绪")
    print("="*60)
    
    print("\n💡 下一步：")
    print("1. 安装MySQL：https://dev.mysql.com/downloads/")
    print("2. 安装Python驱动：pip install mysql-connector-python")
    print("3. 修改DB_CONFIG中的密码")
    print("4. 取消注释代码运行示例")
