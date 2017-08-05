# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import re
import datetime
from scrapy.loader import ItemLoader

from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5


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
        front_image_urls = response.xpath('//div[@class="post-thumb"]//img/@src').extract()
        for post_url, front_image_url in zip(post_urls, front_image_urls):
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail,
                          meta={"front_image_url":front_image_url})
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

        jobble_article_item = JobBoleArticleItem()

        # 文章封面图
        front_image_url = response.meta.get("front_image_url", "")

        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]

        # extract() 方法可以提取 data 项

        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace('·','').strip()

        article_content = response.xpath('//div[@class="entry"]').extract()[0]

        category_tag = response.xpath('//a[@rel="category tag"]/text()').extract()[0]

        match_pattern = '.*?(\d+).*'

        try:
            comment_count = response.xpath('//a[contains(@href,"article-comment")]/text()').extract()[0]

            comment_count = re.match(match_pattern, comment_count)
        except Exception as e:
            comment_count = 0

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

        jobble_article_item["title"] = title
        jobble_article_item['url'] = response.url

        try:
            create_date = datetime.datetime.strptime(create_date, '%Y/%m/%d').date()
        except Exception as e:
            create_date = datetime.datetime.now().date()


        jobble_article_item['create_date'] = create_date
        jobble_article_item['front_image_url'] = [front_image_url]
        jobble_article_item['fav_count'] = fav_count
        jobble_article_item['comment_count'] = comment_count
        jobble_article_item['article_content'] = article_content
        jobble_article_item['category_tag'] = category_tag
        jobble_article_item['url_object_id'] = get_md5(response.url)

        # ----------------------------------------------------
        # 通过 Itemloader 加载 item

        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_xpath('title', '//div[@class="entry-header"]/h1/text()')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_xpath('create_date', '//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_xpath('fav_count', '//i[@class="fa fa-bookmark-o  "]/../text()')
        item_loader.add_value('comment_count', comment_count)
        item_loader.add_xpath('article_content', '//i[@class="fa fa-bookmark-o  "]/../text()')
        item_loader.add_xpath('category_tag', '//div[@class="entry"]')

        # 实例化
        article_item = item_loader.load_item()
        print(article_item)



        yield jobble_article_item

