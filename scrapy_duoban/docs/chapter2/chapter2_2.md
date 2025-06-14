# 第二章 豆瓣影评页面分析与爬虫编写

## 2.5 页面分析

- 入口页：https://movie.douban.com/chart/
- 电影卡片：`.pl2` 区块，包含电影名、评分、详情链接等
- 详情页：包含电影简介、评分、短评、长评列表

## 2.6 主爬虫 douban.py 代码详解

```python name=doubanproject/doubanproject/spiders/douban.py
from lxml import etree
import requests
import scrapy

class DoubanSpider(scrapy.Spider):
    name = 'doubanmovie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/chart/']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }

    def parse(self, response):
        divResultList = response.xpath("//div[@class='pl2']")
        for result in divResultList:
            data = {}
            name = result.xpath(".//a/text()").extract_first() or ''
            name = name.replace('/', '').strip()
            data['name'] = name
            data['aliasName'] = result.xpath(".//a/span/text()").extract_first() or ''
            data['info'] = result.xpath(".//p/text()").extract_first() or ''
            data['rank'] = result.xpath(".//span[@class='rating_nums']/text()").extract_first() or ''
            data['rankPeople'] = result.xpath(".//span[@class='pl']/text()").extract_first() or ''
            data['linkUrl'] = result.xpath(".//a/@href").extract_first() or ''
            yield scrapy.Request(url=data['linkUrl'], callback=self.movieDetail, meta={'data': data}, dont_filter=True)

    def movieDetail(self, response):
        data = response.meta['data']
        movieDetail = {}
        description = response.xpath("//div[@class='indent']/span/text()").extract_first() or ''
        movieDetail['description'] = description.strip()
        data['movieDetail'] = movieDetail

        suffixUrl = response.xpath("//div[@id='hot-comments']/a/@href").extract_first()
        longUrl = response.xpath("//section[@id='reviews-wrapper']/p/a/@href").extract_first()

        longReviewUrl = data['linkUrl'] + longUrl if longUrl else None
        data['longLinkUrl'] = longReviewUrl

        shortReviewUrl = data['linkUrl'] + suffixUrl if suffixUrl else None

        if shortReviewUrl:
            yield scrapy.Request(url=shortReviewUrl, callback=self.shortReview, meta={'data': data}, dont_filter=True)
        else:
            yield data

    def shortReview(self, response):
        data = response.meta['data']
        shortReviewBaseUrl = response.url
        limit = 20
        start = 20
        shortReviewList = []
        while True:
            url = shortReviewBaseUrl + "&start=" + str(start) + "&limit=" + str(limit)
            start = start + 20
            res = requests.get(url=url, headers=self.headers).content.decode('utf8')
            xpathHtml = etree.HTML(res)
            xpathList = xpathHtml.xpath("//div[@class='comment-item']")
            if len(xpathList) < 20:
                break
            for xpathResult in xpathList:
                result = {}
                result['people'] = xpathResult.xpath(".//span[@class='comment-info']/a/text()")
                time_list = xpathResult.xpath(".//span[contains(@class, 'comment-time')]/text()")
                result['time'] = time_list[0].strip() if time_list else ''
                result['content'] = xpathResult.xpath(".//span[@class='short']/text()")
                shortReviewList.append(result)
        data['shortReviewList'] = shortReviewList
        longLinkUrl = data.get('longLinkUrl')
        if longLinkUrl:
            yield scrapy.Request(url=longLinkUrl, callback=self.longReview, meta={'data': data}, dont_filter=True)
        else:
            yield data

    def longReview(self, response):
        data = response.meta['data']
        longReviewUrl = response.url
        start = 20
        longReviewList = []
        while True:
            url = longReviewUrl + "?start=" + str(start)
            start = start + 20
            res = requests.get(url=url, headers=self.headers).content.decode('utf8')
            xpathHtml = etree.HTML(res)
            xpathList = xpathHtml.xpath("//div[@class='main review-item']")
            if len(xpathList) < 20:
                break
            for xpathResult in xpathList:
                result = {}
                result['name'] = xpathResult.xpath(".//header/a[@class='name']/text()")
                result['score'] = xpathResult.xpath(".//span[1]/@title")
                result['time'] = xpathResult.xpath(".//span[2]/text()")
                result['title'] = xpathResult.xpath(".//div[@class='main-bd']/h2/a/text()")
                linkUrlList = xpathResult.xpath(".//div[@class='main-bd']/h2/a/@href")
                linkUrl = str(linkUrlList[0]) if linkUrlList else ''
                result['linkUrl'] = linkUrl
                result['content'] = self.longReviewContentDetail(linkUrl) if linkUrl else {}
                longReviewList.append(result)
        data['longReviewList'] = longReviewList
        yield data

    def longReviewContentDetail(self, url):
        detail = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        res = requests.get(url=url, headers=headers).content.decode('utf8')
        xpathHtml = etree.HTML(res)
        xpathList = xpathHtml.xpath("//div[@id='link-report']")
        if xpathList:
            detail['content'] = str(xpathList[0].xpath(".//p/text()"))
            detail['contentImageUrl'] = xpathList[0].xpath(".//div[@class='image-wrapper']//img/@src")
        else:
            detail['content'] = ''
            detail['contentImageUrl'] = []
        return detail
```

## 2.7 代码说明

- parse()：采集首页电影列表，提取详情链接
- movieDetail()：采集每部电影简介、短评、长评入口
- shortReview()：循环翻页采集短评
- longReview()：循环翻页采集长评，调用 longReviewContentDetail() 采集长评详情
- 数据通过 meta 字典在各 callback 之间传递

> 代码使用 requests + lxml + scrapy 联合解析，适合较复杂的页面和多步采集流程

---