# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
from itemadapter import ItemAdapter


class MoviedoubanspiderPipeline:
    def __init__(self):
        client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        db = client['doubanmovie']
        self.table = db['doubanmovie']

    def process_item(self, item, spider):
        self.table.insert_one(dict(item))
        return item