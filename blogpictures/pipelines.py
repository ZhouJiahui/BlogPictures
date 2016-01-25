# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
import os


class BlogPicturesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        mt={'path':item['path'],'name':item['name']}
        for image_url in item['image_urls'] :
            yield  scrapy.Request(image_url,meta=mt)

    def file_path(self, request, response=None, info=None):
        if  request.meta["name"]!=None:
            return "%s/%s.jpg" %(request.meta['path'],request.meta['name'])
        else:
            name=request.url.split('/')[-1]
            return "%s/%s.jpg" %(request.meta['path'],name)
    

