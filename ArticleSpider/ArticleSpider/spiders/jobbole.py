# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import re


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    # start_urls = ['http://blog.jobbole.com/']
    # http://blog.jobbole.com/112011/
    # http://blog.jobbole.com/all-posts/
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1、获取文章列表页中的文章 url，并交给 scrapy 进行解析
        2、获取下一页的 url，并交给 scrapy 进行下载，下载完成后交给 parse
        :param response:
        :return:
        """
        post_urls = response.xpath('//a[@class="archive-title"]/@href').extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail,
                          meta={"front_image_url":})
            # print(post_url)

        # 提取下一页并交给 scrapy 下载
        next_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)


    def parse_detail(self, response):
        """
        提取文章的具体字段
        :param response:
        :return:
        """

        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]

        # extract() 方法可以提取 data 项

        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace('·','').strip()

        article_content = response.xpath('//div[@class="entry"]').extract()[0]

        category_tag = response.xpath('//a[@rel="category tag"]/text()').extract()[0]

        match_pattern = '.*?(\d+).*'

        comment_count = response.xpath('//a[contains(@href,"article-comment")]/text()').extract()[0]

        comment_count = re.match(match_pattern, comment_count)

        if comment_count:
            comment_count = int(comment_count.group(1))
        else:
            comment_count = 0

        fav_count = response.xpath('//i[@class="fa fa-bookmark-o  "]/../text()').extract()[0]

        fav_count = re.match(match_pattern, fav_count)

        if fav_count:
            fav_count = int(fav_count.group(1))
        else:
            fav_count = 0

        pass
