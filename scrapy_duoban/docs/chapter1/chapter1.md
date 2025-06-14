# 第一章 Scrapy简介与环境准备

## 1.1 Scrapy简介

Scrapy 是 Python 编写的高效爬虫框架，广泛应用于网页数据采集，支持异步、多线程、分布式等特性，非常适合豆瓣影评这类结构化页面的数据抓取。

## 1.2 环境准备

### 1.2.1 安装 Python

推荐 Python 3.7 及以上，Windows、macOS、Linux 均可。

### 1.2.2 安装 Scrapy 及常用依赖

```bash
pip install scrapy lxml requests pymongo fake-useragent
```

如需用 MongoDB 存储，提前本地安装并启动 MongoDB。

### 1.2.3 项目结构参考

你可以通过如下命令创建 Scrapy 项目（建议英文目录，不要用“蜘蛛”中文名）：

```bash
scrapy startproject doubanproject
```

结构如图：

```
doubanproject/
  scrapy.cfg
  doubanproject/
    __init__.py
    items.py
    middlewares.py
    pipelines.py
    settings.py
    spiders/
      __init__.py
```


