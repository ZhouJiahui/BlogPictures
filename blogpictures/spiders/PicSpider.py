#-*- coding:utf-8 -*-
import scrapy
import os
import re
import sys
from blogpictures.items import BlogPicturesItem

class PicSpider(scrapy.spiders.Spider):
    name = "SinaPicture"
    orgin="http://photo.blog.sina.com.cn"
    start_urls = []
    
    def __init__(self,userlist=None):
        if userlist==None or userlist=="":
            print '[There need an userlist.]'
        else:
            self.start_urls=userlist.split(";")
        
    def start_requests(self):
        for url in self.start_urls:
            href=self.orgin+"/"+url
            yield scrapy.Request(href, meta={'path':url},callback=self.name_parse)
            
    def name_parse(self, response):
        sels=response.xpath("//span[contains(@class,'SG_dot')]")
        if len(sels)>=2:
            sels=sels[1].xpath("a/@href")
            if len(sels)!=0:
                href=sels.extract()[0]
                href=self.orgin+href
                return [scrapy.Request(href, meta=response.meta,callback=self.category_parse)]
    
    def category_parse(self, response):
        sels=response.xpath("//div[contains(@class,'pt_border_bg')]/p")
        for sel in sels:
                href=sel.xpath("a/@href")
                if len(href)!=0:
                    href=href.extract()[0]
                else:
                    continue
                title=sel.xpath("a/img/@title")
                if len(title)!=0:
                    title=title.extract()[0]
                else:
                    continue
                path=response.meta['path']+'/'+title
                yield scrapy.Request(url=href, meta={'path':path},callback=self.album_parse)

        sels=response.xpath("//ul[contains(@class,'SG_pages')]")
        if len(sels)!=0:
            nxts=sels.re('<a href="([^"]+)"[^>]+>'+u"下一页")
            if len(nxts)!=0:
                nxt=nxts[0]
                yield scrapy.Request(url=nxt, meta=response.meta,callback=self.category_parse)
       
    def album_parse(self, response):
        sels=response.xpath("//div[contains(@class,'pt_border')]/p")
        for sel in sels:
                href=sel.xpath("a/@href")
                if len(href)!=0:
                    href=href.extract()[0]
                else:
                    continue
                title=sel.xpath("a/img/@title")
                if len(title)!=0:
                    title=title.extract()[0]
                else:
                    continue
                yield scrapy.Request(url=href, meta={'path':response.meta['path'],'name':title},callback=self.picture_parse)
        
        sels=response.xpath("//div[contains(@class,'pt_title_sub SG_txta')]")
        for sel in sels:
                href=sel.xpath("a/@href")
                if len(href)!=0:
                    href=href.extract()[0]
                else:
                    continue
                title=sel.xpath("a/text()")
                if len(title)!=0:
                    title=title.extract()[0]
                else:
                    continue
                path=response.meta['path']+"/"+title
                yield scrapy.Request(url=href, meta={'path':path},callback=self.content_parse)
                
        sels=response.xpath("//ul[contains(@class,'SG_pages')]")
        if len(sels)!=0:
            nxts=sels.re('<a href="([^"]+)"[^>]+>'+u"下一页")
            if len(nxts)!=0:
                nxt=nxts[0]
                yield scrapy.Request(url=nxt, meta=response.meta,callback=self.album_parse)

    def content_parse(self,response):
        sels=response.xpath("//div[contains(@class,'articalContent')]")
        if len(sels)!=0:
            hrefs=list()
            seq=sels[0].extract().encode("utf-8")
            match=m=re.findall('<a href="[^&]+&amp;url=([^"]+)" target="_blank">',seq,re.I|re.M)
            if len(match)!=0:
                item=BlogPicturesItem()
                item['path']=response.meta['path']
                item['name']=None
                item['image_urls']=list()
                for href in match:
                    item['image_urls'].append(href)
                return item
            
    
    def picture_parse(self,response):
        sels=response.xpath("//a[contains(@onclick,'sendLog')]/@href")
        if len(sels)!=0:
            url=sels.extract()[0]
            item=BlogPicturesItem()
            item['path']=response.meta['path']
            item['name']=response.meta['name']
            item['image_urls']=list()
            item['image_urls'].append(url)
            return item
