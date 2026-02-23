# 🕷️ Python爬虫入门示例

作者：夕语  
日期：2026-02-23

---

## 📁 文件说明

| 文件 | 说明 | 适用场景 |
|------|------|----------|
| `basic_crawler.py` | 基础爬虫 | 静态网页、简单数据提取 |
| `browser_crawler.py` | 浏览器自动化爬虫 | 动态网页、JavaScript渲染、需要交互的网站 |
| `requirements.txt` | 依赖包列表 | 安装所需Python库 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 进入项目目录
cd python-crawler-examples

# 安装依赖包
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install
```

### 2. 运行基础爬虫

```bash
python basic_crawler.py
```

### 3. 运行浏览器爬虫

```bash
python browser_crawler.py
```

---

## 📚 功能说明

### 基础爬虫 (`basic_crawler.py`)

**功能：**
- ✅ HTTP请求获取网页
- ✅ HTML解析（BeautifulSoup）
- ✅ 数据提取（标题、链接、文本）
- ✅ 数据保存（JSON/TXT）
- ✅ 自动重试机制

**适用场景：**
- 新闻网站
- 博客文章
- 静态网页
- API数据获取

**示例代码：**
```python
from basic_crawler import crawl_website

# 爬取网页
result = crawl_website('https://www.python.org', 
                       parse_type='general', 
                       output_format='json')
```

---

### 浏览器爬虫 (`browser_crawler.py`)

**功能：**
- ✅ 浏览器自动化（Playwright）
- ✅ JavaScript渲染支持
- ✅ 模拟用户交互（点击、输入）
- ✅ 无限滚动处理
- ✅ 反检测模式
- ✅ 截图保存

**适用场景：**
- 单页应用（SPA）
- 需要登录的网站
- 动态加载内容
- 需要交互操作

**示例代码：**
```python
from browser_crawler import crawl_with_browser

# 基础爬取
result = crawl_with_browser('https://www.example.com')

# 模拟搜索
from browser_crawler import simulate_user_interaction
result = simulate_user_interaction('https://www.bing.com', 
                                   search_keyword='Python')
```

---

## 🛠️ 常用技巧

### 1. 查找元素选择器

```python
# CSS选择器
page.query_selector('.class-name')
page.query_selector('#id-name')
page.query_selector('div > p')

# XPath（需要额外库）
from playwright.sync_api import Route
```

### 2. 等待元素加载

```python
# 等待元素出现
page.wait_for_selector('.target-element')

# 等待网络空闲
page.wait_for_load_state('networkidle')

# 等待特定时间
time.sleep(2)
```

### 3. 处理反爬

```python
# 设置请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0...',
    'Referer': 'https://www.google.com/'
}

# 添加延迟
time.sleep(random.uniform(1, 3))

# 使用代理（需要代理服务）
context = browser.new_context(
    proxy={'server': 'http://proxy.example.com:8080'}
)
```

---

## ⚠️ 注意事项

1. **遵守robots.txt** - 爬取前检查网站的robots.txt文件
2. **控制频率** - 不要频繁请求，避免给服务器造成压力
3. **合法合规** - 仅爬取公开数据，遵守相关法律法规
4. **尊重版权** - 不要滥用爬取的数据

---

## 📖 学习资源

- [Requests文档](https://requests.readthedocs.io/)
- [BeautifulSoup文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Playwright文档](https://playwright.dev/python/)
- [Scrapy文档](https://scrapy.org/)

---

## 🔧 常见问题

### Q: 安装Playwright失败？
```bash
# 尝试使用国内镜像
pip install playwright -i https://pypi.tuna.tsinghua.edu.cn/simple
playwright install --with-deps
```

### Q: 中文乱码？
```python
# 设置正确的编码
response.encoding = response.apparent_encoding
```

### Q: 被网站封锁？
- 降低爬取频率
- 使用代理IP
- 模拟真实用户行为
- 更换User-Agent

---

## 📝 下一步

1. 学习Scrapy框架（大型爬虫项目）
2. 了解分布式爬虫
3. 学习数据清洗和处理
4. 实践真实项目

---

祝您学习顺利！如有问题，随时联系夕语。🤖
