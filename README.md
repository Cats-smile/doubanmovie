# 豆瓣电影
 A crawler of doubamovie 
 
 一个小小的入门级scrapy框架的应用，选取豆瓣电影对排行榜前1000的电影数据进行爬取。
# spider.py
start_requests方法为scrapy的方法，我们对它进行重写。

    def start_requests(self):
        # 将start_url中的链接通过for循环进行遍历。
        for url in self.start_urls:
            # 通过yield发送Request请求。
            # 这里的Reques注意是scrapy下的Request类。注意不到导错类了。
            # 这里的有3个参数：
            #        1、url为遍历后的链接
            #        2、callback为发送完请求后通过什么方法进行处理，这里通过parse方法进行处理。
            #        3、如果网站设置了防爬措施，需要加上headers伪装浏览器发送请求。

            yield scrapy.Request(url=url, callback=self.parse, headers=self.headler)

使用scrapy的css选择器，定位选取范围div.item

重写parse对start_request()请求到的数据进行处理，通过yield对爬取到的网页数据进行封装

    def parse(self, response):
        # 这里使用scrapy的css选择器，既然数据在class为item的div下，那么把选取范围定位div.item
        for quote in response.css('div.item'):
            # 通过yield对网页数据进行循环抓取
            yield {
                # 抓取排名、电影名、导演、主演、上映日期、制片国家 / 地区、类型，评分、评论数量、一句话评价以及电影链接
                "电影链接": quote.css('div.info div.hd a::attr(href)').extract_first(),
                "排名": quote.css('div.pic em::text').extract(),
                "电影名": quote.css('div.info div.hd a span.title::text')[0].extract(),
                "上映年份": quote.css('div.info div.bd p::text')[1].extract().split('/')[0].strip(),
                "制片国家": quote.css('div.info div.bd p::text')[1].extract().split('/')[1].strip(),
                "类型": quote.css('div.info div.bd p::text')[1].extract().split('/')[2].strip(),
                "评分": quote.css('div.info div.bd div.star span.rating_num::text').extract(),
                "评论数量": quote.css('div.info div.bd div.star span::text')[1].re(r'\d+'),
                "引言": quote.css('div.info div.bd p.quote span.inq::text').extract(),
            }
        next_url = response.css('div.paginator span.next a::attr(href)').extract()
        if next_url:
            next_url = "https://movie.douban.com/top250" + next_url[0]
            print(next_url)
            yield scrapy.Request(next_url, headers=self.headler)

# pipelines.py
将其存入mongodb数据库中，不用提前创建表。

    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        scrapy_db = self.client['doubanmovie']  # 创建数据库
        self.coll = scrapy_db['movie']  # 创建数据库中的表格

    def process_item(self, item, spider):
        self.coll.insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

# item.py
数据封装

    url = scrapy.Field()
    name = scrapy.Field()
    order = scrapy.Field()
    content = scrapy.Field()
    contentnum = scrapy.Field()
    year = scrapy.Field()
    country = scrapy.Field()
    score = scrapy.Field()
    vary = scrapy.Field()
