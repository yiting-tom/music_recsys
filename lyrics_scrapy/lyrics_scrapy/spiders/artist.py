import scrapy


class ArtistSpider(scrapy.Spider):
    name = 'artist'
    allowed_domains = ['https://mojim.com']
    start_urls = ['http://https/']

    def parse(self, response):
        pass
