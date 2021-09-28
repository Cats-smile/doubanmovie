# -*- coding:utf-8 -*-
import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'douban2'

    start_urls = ['https://movie.douban.com/top250']

    headler = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                      'Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headler)

    def parse(self, response):

        for href in response.css('div.item div.info div.hd a::attr(href)').extract():
            yield scrapy.Request(href, headers=self.headler,
                                 callback=self.parse_author)

        next_url = response.css('div.paginator span.next a::attr(href)').extract()
        if next_url:
            next_url = "https://movie.douban.com/top250" + next_url[0]
            print(next_url)
            yield scrapy.Request(next_url, headers=self.headler, callback=self.parse)

    def parse_author(self, response):
        # 通过yield对网页数据进行循环抓取
        content = response.xpath("//*[@id='link-report']/span[1]/span/text()[1]").extract()
        content2 = response.xpath('//div[contains(@id,"ident")]/span[contains(@property,"v:summary")]/text()')
        print("------------------------------------")
        print(content2)
        print("------------------------------------")
        yield {
            '排名': response.css('.top250-no::text').extract(),
            '电影名': response.xpath('//span[contains(@property,"v:itemreviewed")]/text()').extract(),
            '导演': response.xpath(
                '//div[contains(@id,"info")]/span[1]/span[contains(@class,"attrs")]/a/text()').extract(),
            '编剧': response.xpath(
                '//div[contains(@id,"info")]/span[2]/span[contains(@class,"attrs")]/a/text()').extract(),
            '主演': response.xpath(
                '//div[contains(@id,"info")]/span[3]/span[contains(@class,"attrs")]/a/text()').extract(),
            '语言': response.xpath(
                '//div[contains(@id,"info")]/span[contains(@class,"pl")][3]/following::text()[1]').extract(),
            '上映日期': response.xpath(
                '//div[contains(@id,"info")]/span[contains(@property,"v:initialReleaseDate")]/text()').extract(),
            '片长': response.xpath('//div[contains(@id,"info")]/span[contains(@property,"v:runtime")]/text()').extract(),
        }
