# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from Image_Crawl.items import ImageItem


class ImgcrawlSpider(scrapy.Spider):
    name = 'imgcrawl'
    allowed_domains = ['http://www.win4000.com']
    start_urls = ['http://www.win4000.com/wallpaper_detail_145479.html']

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    }

    def parse(self, response):
        # with open("text.html", "wb") as f:
        #     f.write(response.body)

        # image_item = ImageItem()

        next_url = response.xpath('//div[@class="pic-next-img"]/a/@href').extract()[0]

        items_loader = ItemLoader(item=ImageItem(), response=response)

        items_loader.add_xpath("next_url", '//div[@class="pic-next-img"]/a/@href')
        items_loader.add_xpath("img_url", '//div[@class="pic-meinv"]/a/img/@src')
        items_loader.add_xpath("img_title", '//div[@class="ptitle"]/h1/text()')
        items_loader.add_xpath("img_size", '//span[@class="size"]/em/text()')
        items_loader.add_xpath("img_upload_time", '//span[@class="time"]/text()')

        image_item = items_loader.load_item()
        image_item['img_base64'] = ''

        yield scrapy.Request(url=next_url, callback=self.parse, headers=self.headers, dont_filter=True)
        yield image_item

        pass
