import scrapy
from moviescripts.items import MoviescriptsItem


class MoviescriptsSpider(scrapy.Spider):
    name = "moviescripts"
    allowed_domains = ["imsdb.com"]
    start_urls = [
       'http://www.imsdb.com/all%20scripts/'
    ]

    def parse(self, response):
        for name in response.xpath('//p/a'):
            next_name = name.xpath('@href').extract_first()
            next_page = response.urljoin(next_name)
            title = name.xpath('@title').extract_first()[:-7]
            meta={'title':title,}
            yield scrapy.Request(next_page, callback=self.parse2,meta=meta)
            

    def parse2(self, response):
        next_page = response.xpath('//p/a[contains(@href, "scripts")]/@href').extract_first()
        next_page = response.urljoin(next_page)
        item = MoviescriptsItem()
        item['title']=response.meta['title']
        item['link']=next_page
        yield item
            
#==============================================================================
#     def parse3(self, response):
#         script = response.xpath('//pre/b')
#         item = MoviescriptsItem()
#         item['title'] = response.meta['title']
#         item['zcontent'] = script.extract()
#         yield item
#   #      yield script.extract_first()
#  #       return script.extract_first()
# 
#==============================================================================
