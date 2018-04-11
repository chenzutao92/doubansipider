# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader

from doubansipider.items import DoubansipiderItem, MovieItemLoader

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        """
            1. 获取电影列表页中的电影url并交给scrapy下载后并进行解析
            2.获取下一页的Url并交给scrapy进行下载，下载完成后交给parse
        """
        # 获取电影url
        post_nodes = response.css(".grid_view .hd a::attr(href)").extract()
        for post_node in post_nodes:
            # 如果url不包括主域名，需要拼接
            yield Request(url=parse.urljoin(response.url, post_node), callback=self.parse_detail)
            # yield Request(url=post_node, callback=self.parse_detail)

        next_url = response.css(".paginator .next a::attr(href)").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        text_xpath = "//*[@id='info']/text()"
        text = [element.strip() for element in response.xpath(text_xpath).extract()]
        while "" in text:
            text.remove("")
        while "/" in text:
            text.remove("/")
        item_loader = MovieItemLoader(item=DoubansipiderItem(), response=response)
        item_loader.add_value('url', response.url)
        item_loader.add_xpath('name', '//*[@id="content"]/h1/span[@property="v:itemreviewed"]/text()')
        item_loader.add_css('director', '#info > span:nth-child(1) > span.attrs > a::text')
        item_loader.add_css('scriptwriter', '#info > span:nth-child(3) > span.attrs > a::text')
        item_loader.add_css('protagonist', '#info > span.actor > span.attrs > a::text')
        item_loader.add_xpath('movie_type', '//*[@id="info"]/span[@property="v:genre"]/text()')
        item_loader.add_value('region', text[0])
        item_loader.add_value('language', text[1])
        item_loader.add_xpath('release_data', '//*[@id="info"]/span[@property="v:initialReleaseDate"]/text()')
        item_loader.add_xpath('mins', '//*[@id="info"]/span[@property="v:runtime"]/text()')
        item_loader.add_value('alternate_name', text[2])
        item_loader.add_xpath('No', '//*[@id="content"]/div[1]/span[1]/text()')
        item_loader.add_xpath('graded', '//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
        item_loader.add_xpath('comment', '//span[@property="v:votes"]/text()')
        item_loader.add_xpath('synopsis', '//span[@property="v:summary"]/text()')

        movieItem = item_loader.load_item()
        yield movieItem