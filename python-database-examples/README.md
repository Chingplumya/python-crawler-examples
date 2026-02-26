# 📚 第二阶段：数据库与存储

**学习周期：** 2-3周  
**前置知识：** Python基础、爬虫基础

---

## 📋 学习大纲

| 周次 | 主题 | 内容 | 实战项目 |
|------|------|------|----------|
| **第1周** | MySQL基础 | 连接、CRUD、事务、索引 | 爬虫数据入库系统 |
| **第2周** | PostgreSQL | JSON支持、高级查询 | 新闻数据分析 |
| **第3周** | 对象存储 | OSS/S3、文件管理 | 图片/文件存储系统 |

---

## 🗓️ 第1周：MySQL基础

### 学习目标
- ✅ 安装和配置MySQL
- ✅ 掌握SQL基本语法
- ✅ 理解事务和索引
- ✅ 实现爬虫数据入库

### 每日计划

#### Day 1-2: 环境搭建
- [ ] 安装MySQL 8.0
- [ ] 安装MySQL Workbench（图形化管理工具）
- [ ] 安装Python驱动：`pip install mysql-connector-python`
- [ ] 创建第一个数据库

**安装命令（Ubuntu）：**
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

**安装命令（Windows）：**
- 下载：https://dev.mysql.com/downloads/installer/
- 选择"Developer Default"
- 记住root密码

#### Day 3-4: SQL基础
- [ ] CREATE DATABASE / TABLE
- [ ] INSERT / SELECT / UPDATE / DELETE
- [ ] WHERE条件查询
- [ ] ORDER BY排序
- [ ] LIMIT限制结果

**练习代码：** `mysql_basics.py`

#### Day 5-6: 高级特性
- [ ] 索引优化
- [ ] 事务处理
- [ ] 多表连接（JOIN）
- [ ] 聚合函数（COUNT, SUM, AVG）

#### Day 7: 实战项目
- [ ] 完成`crawler_with_db.py`
- [ ] 爬取10个网页并入库
- [ ] 实现去重功能
- [ ] 导出数据到JSON

---

## 🗓️ 第2周：PostgreSQL

### 学习目标
- ✅ 安装PostgreSQL
- ✅ 掌握JSON数据类型
- ✅ 学习全文搜索
- ✅ 对比MySQL和PostgreSQL

### 每日计划

#### Day 1-2: PostgreSQL基础
- [ ] 安装PostgreSQL
- [ ] 基本SQL语法（与MySQL类似）
- [ ] 特有数据类型（ARRAY, JSON, JSONB）

#### Day 3-4: JSON支持
- [ ] JSONB存储
- [ ] JSON查询操作符
- [ ] 在爬虫数据中的应用

**示例：**
```sql
-- 存储JSON数据
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    metadata JSONB
);

-- 查询JSON字段
SELECT * FROM articles 
WHERE metadata->>'author' = 'John';
```

#### Day 5-6: 全文搜索
- [ ] 创建全文索引
- [ ] 搜索查询
- [ ] 相关性排序

#### Day 7: 实战项目
- [ ] 用PostgreSQL存储新闻数据
- [ ] 实现关键词搜索
- [ ] 对比MySQL性能

---

## 🗓️ 第3周：对象存储

### 学习目标
- ✅ 理解对象存储概念
- ✅ 使用阿里云OSS/亚马逊S3
- ✅ 实现文件上传下载
- ✅ 集成到爬虫系统

### 每日计划

#### Day 1-2: 对象存储基础
- [ ] 什么是对象存储
- [ ] vs 块存储 vs 文件存储
- [ ] 主流服务商对比

| 服务商 | 产品名 | 免费额度 | 价格 |
|--------|--------|----------|------|
| 阿里云 | OSS | 40GB/年 | ¥0.12/GB/月 |
| 腾讯云 | COS | 50GB/年 | ¥0.11/GB/月 |
| 亚马逊 | S3 | 5GB/月 | $0.023/GB/月 |
| 七牛云 | Kodo | 10GB永久 | ¥0.09/GB/月 |

#### Day 3-4: 阿里云OSS实战
- [ ] 注册阿里云账号
- [ ] 创建Bucket
- [ ] 获取AccessKey
- [ ] Python SDK使用

**安装SDK：**
```bash
pip install oss2
```

**上传文件示例：**
```python
import oss2

auth = oss2.Auth('AccessKeyId', 'AccessKeySecret')
bucket = oss2.Bucket(auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'my-bucket')

# 上传文件
bucket.put_object('files/test.txt', b'Hello World')

# 下载文件
obj = bucket.get_object('files/test.txt')
print(obj.read().decode('utf-8'))
```

#### Day 5-6: 集成到爬虫
- [ ] 爬取图片并上传OSS
- [ ] 数据库存储URL
- [ ] 实现CDN加速

#### Day 7: 综合项目
- [ ] 完整爬虫系统
- [ ] 数据存MySQL
- [ ] 图片存OSS
- [ ] 提供API查询

---

## 📁 项目文件说明

```
python-database-examples/
├── mysql_basics.py          # MySQL基础操作
├── crawler_with_db.py       # 爬虫入库系统
├── postgresql_examples.py   # PostgreSQL示例（待创建）
├── oss_storage.py           # 对象存储示例（待创建）
└── README.md                # 本文档
```

---

## 🎯 学习检查点

### 第1周结束时应能：
- ✅ 独立创建MySQL数据库和表
- ✅ 编写复杂SQL查询
- ✅ 实现爬虫数据去重入库
- ✅ 使用事务保证数据一致性

### 第2周结束时应能：
- ✅ 使用PostgreSQL存储JSON数据
- ✅ 实现全文搜索功能
- ✅ 根据场景选择MySQL或PostgreSQL

### 第3周结束时应能：
- ✅ 配置和使用对象存储
- ✅ 实现文件上传下载
- ✅ 构建完整的爬虫存储系统

---

## 📖 推荐资源

### 官方文档
- [MySQL文档](https://dev.mysql.com/doc/)
- [PostgreSQL文档](https://www.postgresql.org/docs/)
- [阿里云OSS文档](https://help.aliyun.com/product/31815.html)

### 在线教程
- [菜鸟教程 - MySQL](https://www.runoob.com/mysql/mysql-tutorial.html)
- [廖雪峰 - SQL教程](https://www.liaoxuefeng.com/wiki/1177760294764384)

### 练习平台
- [SQLZoo](https://sqlzoo.net/) - 在线SQL练习
- [LeetCode Database](https://leetcode.com/problemset/database/) - 数据库题库

---

## 💡 学习建议

1. **多动手** - 每个概念都要写代码验证
2. **理解原理** - 不要死记硬背SQL语句
3. **对比学习** - MySQL和PostgreSQL对比着学
4. **项目驱动** - 用实际项目巩固知识
5. **记录笔记** - 把遇到的问题记录下来

---

## ❓ 常见问题

### Q: MySQL和PostgreSQL选哪个？
**A:** 
- **MySQL** - 简单、快速、适合Web应用
- **PostgreSQL** - 功能强大、支持复杂查询、适合数据分析

### Q: 本地安装太麻烦，有替代方案吗？
**A:** 
- 使用Docker：`docker run --name mysql -e MYSQL_ROOT_PASSWORD=123456 -p 3306:3306 -d mysql:8`
- 使用云数据库（阿里云、腾讯云都有免费试用）

### Q: 数据量多大需要考虑优化？
**A:** 
- 单表超过100万行考虑分表
- 查询超过1秒考虑加索引
- 写入频繁考虑读写分离

---

**开始学习吧！有问题随时找我。** 🚀
