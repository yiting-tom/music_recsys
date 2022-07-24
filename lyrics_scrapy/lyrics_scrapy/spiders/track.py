import scrapy


class TrackSpider(scrapy.Spider):
    name = 'track'
    allowed_domains = ['mojim.com']
    start_urls = 

    def parse(self, response):
        pass
