# 第二章 Scrapy项目结构与基本用法

## 2.1 Scrapy 项目结构说明

- scrapy.cfg：项目配置入口，运行爬虫时需要位于该目录
- doubanproject/：主模块，含爬虫、item、pipeline、middleware、settings
- spiders/：所有爬虫脚本（如 douban.py）
- items.py：定义数据结构（Item）
- pipelines.py：数据存储管道（如存 MongoDB）
- middlewares.py、UserAgentMiddleware.py：爬虫中间件（如代理池、UA池）

## 2.2 新建爬虫

Scrapy 官方建议用命令行自动生成爬虫模板。  
具体命令如下：

```bash
scrapy genspider doubanmovie movie.douban.com
```

- 这条命令会在你的 spiders 目录下，自动生成一个名为 doubanmovie.py 的爬虫文件，初始模板已经帮你写好了一些基本结构。
- doubanmovie 是爬虫的名字，movie.douban.com 是你要爬取的域名。

### 提示

我的实际项目里，主爬虫文件是 douban.py（即路径为 doubanproject/doubanproject/spiders/douban.py），不是用命令自动生成的 doubanmovie.py，而是我自己手写或重命名的。

> 总结：  
> 推荐命令 `scrapy genspider doubanmovie movie.douban.com` 是官方建议的标准化创建爬虫文件的方法。  
> 我的项目实际爬虫主脚本名字是 douban.py，不影响功能，只是名字不同（内容要符合 Scrapy 的 Spider 类格式即可）。  
> 你可以继续用你已有的 doubanmovie.py，只要名字和 settings.py 里的 name 属性一致，不会有任何问题。

## 2.3 运行爬虫

命令行进入含有 scrapy.cfg 的项目根目录，运行：

```bash
scrapy crawl doubanmovie
```
如要导出为 json/csv：
```bash
scrapy crawl doubanmovie -o result.json
```

## 2.4 主要依赖说明

- lxml、requests：用于部分页面请求和 HTML 解析
- pymongo：写入 MongoDB
- fake-useragent：自动切换 UA，模拟浏览器防止反爬

> 具体依赖和代码已在项目中体现，后续章节详细讲解