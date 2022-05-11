import scrapy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from openseaproject.items import OpenseaprojectItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SnipertopSpider(scrapy.Spider):
    name = 'sniperTop'
    allowed_domains = ['opensea.io']
    start_urls = 'https://opensea.io/rankings'

    def start_requests(self):
        for pageNum in range(0, self.settings.get('MAX_PAGE_NUM')):
            print('7777777' + str(pageNum))
            yield scrapy.Request(url=self.start_urls, callback=self.parse, meta={'page': pageNum}, dont_filter=True)


    # allowed_domains = ['jd.com']
    # start_urls = ['https://search.jd.com/Search?keyword=python%E7%88%AC%E8%99%AB&suggest=1.his.0.0&wq=python%E7%88%AC%E8%99%AB&page=1']

    def parse(self, response):
        print('爬取Top信息....')
        item = OpenseaprojectItem()
        # base_list = response.xpath('//*[@id="main"]/div/div[2]/div/div[3]/div').extract()
        # normalize-space(//*[@id="main"]/div/div[1]/p)
        base_list = response.xpath('//*[@id="main"]/div/div[2]/div/div[3]/div')
        # base_list1 = response.xpath('//*[@id="main"]/div/div[3]/button[2]').extract_first()

        for nodeList in base_list:
            item['rankNo'] = nodeList.xpath('normalize-space(./a/div[1]/div[1]/span/div)').extract_first()
            item['name'] = nodeList.xpath('normalize-space(./a/div[1]/div[3]/span/div)').extract_first()
            item['img'] = nodeList.xpath('normalize-space(./a/div[1]/div[2]/div[1]/div/img/@src)').extract_first()
            item['uri'] = 'https://opensea.io' + nodeList.xpath('normalize-space(./a/@href)').extract_first()
            item['volume'] = nodeList.xpath('normalize-space(./a/div[2]/div/span/div)').extract_first()
            item['dd24h'] = nodeList.xpath('normalize-space(./a/div[3]/div/span/div)').extract_first()
            item['dd7D'] = nodeList.xpath('normalize-space(./a/div[4]/div/span/div)').extract_first()
            item['floorPrice'] = nodeList.xpath('normalize-space(./a/div[5]/div/span/div)').extract_first()
            item['owners'] = nodeList.xpath('normalize-space(./a/div[7]/p)').extract_first()
            yield item


