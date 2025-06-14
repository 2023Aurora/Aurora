# 第三章 数据存储与清洗

## 3.1 Items 数据结构定义

在 items.py 定义：

```python name=doubanproject/doubanproject/items.py
import scrapy

class DoubanprojectItem(scrapy.Item):
    title = scrapy.Field()   # 电影名字
    content = scrapy.Field() # 电影信息
    infi = scrapy.Field()    # 电影简介
    score = scrapy.Field()   # 电影评分
```

## 3.2 Pipelines 数据写入 MongoDB

pipelines.py 代码：

```python name=doubanproject/doubanproject/pipelines.py
import pymongo

class MoviedoubanspiderPipeline:
    def __init__(self):
        client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        db = client['doubanmovie']
        self.table = db['doubanmovie']

    def process_item(self, item, spider):
        self.table.insert_one(dict(item))
        return item
```

settings.py 配置：

```python name=doubanproject/doubanproject/settings.py
ITEM_PIPELINES = {
   'doubanproject.pipelines.MoviedoubanspiderPipeline': 300,
}
```

## 3.3 简单清洗建议

- 对字符串 strip()
- 处理 None、空字符串为默认值
- 短评、长评列表建议用 json/dict 存到数据库

---

## 3.4 导出与分析

- 可用 pandas 读取 json/csv
- 也可直接用 MongoDB 可视化工具查看