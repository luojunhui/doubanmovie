# -*- coding: utf-8 -*-
# 引用python自带的json
import json

import scrapy
# 引用我们定义好的item模型
from ..items import DoubanmovieItem


class DoubanSpider(scrapy.Spider):
    # 这个spider(蜘蛛的名字)
    name = 'douban'
    # 不在此允许范围内的域名就会被过滤,不会进行爬取,其实这个可要可不要
    allowed_domains = ['movie.douban.com']
    # 这是入口
    start_urls = ['https://movie.douban.com/j/search_tags?type=movie&source=']
    # 定义电影详情url
    movie_info_url = 'https://movie.douban.com/j/search_subjects?' \
                     'type=movie&tag={tag}&sort=recommend&page_limit={page_limit}&page_start={page_start}'

    # 定义将要爬取前3页的数据
    page_size = 3

    # 从start_urls获取第一个url访问后会进入这个方法
    def parse(self, response):
        # body_as_unicode能尽量返回文本是unicode的,比较好处理
        body = response.text
        # 字符串转json
        obj = json.loads(body)
        tags = obj.get('tags', [])
        for tag in tags:
            cur_page = 1
            # 定义meta,可以传递参数到下一个方法中
            meta = dict(tag=tag,  # 电影类型
                        page_limit=20,  # 展示电影的数量
                        page_start=(cur_page - 1) * 20,  # 从第几条记录开始
                        cur_page=cur_page
                        )
            # 生成每个类型下的第一页的电影列表url
            first_page_url = self.movie_info_url.format(**meta)
            yield scrapy.Request(url=first_page_url, callback=self.parse_movie_list_page, meta=meta)

    # 解析电影列表
    def parse_movie_list_page(self, response):
        # parse里定义的meta
        meta = response.meta

        body = response.text
        obj = json.loads(body)
        subjects = obj.get('subjects', [])
        # 将列表里的电影信息提取出来
        for movie in subjects:
            item = DoubanmovieItem()
            item['name'] = movie['title']
            item['rate'] = movie['rate']
            item['tag'] = meta['tag']
            yield item

        # 进行翻页请求,本文只作参考,所以就爬前三页内容后停止,不要给网站造成太多压力
        cur_page = meta['cur_page']
        if cur_page < self.page_size:
            meta['cur_page'] = cur_page + 1
            meta['page_start'] = (meta['cur_page'] - 1) * 20
            next_page_url = self.movie_info_url.format(**meta)
            # 这里的回调还是本方法,因为格式都没有变动,只是内容变了
            yield scrapy.Request(url=next_page_url, callback=self.parse_movie_list_page, meta=meta)
