import scrapy


class MojimSpider(scrapy.Spider):
    name = 'mojim'
    allowed_domains = ['mojim.com']
    start_urls = ['https://mojim.com/uszlistALLTime.htm']

    def parse(self, response):
        pass

    def __get_all_
