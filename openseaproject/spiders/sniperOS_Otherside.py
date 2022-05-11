import scrapy
from openseaproject.items import OS_Otherside
import openpyxl


class SnipertopSpider(scrapy.Spider):
    name = 'sniperOS_Otherside'
    allowed_domains = ['opensea.io']
    start_urls = 'https://opensea.io/assets/0x34d85c9cdeb23fa97cb08333b511ac86e1c4e258/'
    start_page = 0
    end_page = 0

    def __init__(self,start_page = None,end_page = None,*args, **kwargs):
        print('start_page = '+start_page+';end_page = '+end_page)
        self.start_page = int(start_page)
        self.end_page = int(end_page)

    def start_requests(self):
        excel_file = openpyxl.load_workbook('./otherside_data.xlsx')
        sheet = excel_file['Sheet1']
        num = sheet.max_row


        for pageNum in range(self.start_page, self.end_page):
            cell = sheet['A' + str(pageNum)]
            uri = self.start_urls+str(cell.value)
            print('7777777' + str(cell.value))
            yield scrapy.Request(url=uri, callback=self.parse, dont_filter=True)


    # allowed_domains = ['jd.com']
    # start_urls = ['https://search.jd.com/Search?keyword=python%E7%88%AC%E8%99%AB&suggest=1.his.0.0&wq=python%E7%88%AC%E8%99%AB&page=1']

    def parse(self, response):
        print('爬取Top信息....')
        item = OS_Otherside()
        name_add = response.xpath('normalize-space(//*[@id="main"]/div/div/div/div[1]/div/div[1]/div[2]/section[2]/div[1]/div/a/span)').extract_first()
        rank_add = response.xpath('normalize-space(//*[@id="main"]/div/div/div/div[1]/div/div[1]/div[2]/section[1]/h1)').extract_first()
        item['address'] = name_add
        item['rankNo'] = rank_add
        yield item

        # base_list = response.xpath('//*[@id="main"]/div/div[2]/div/div[3]/div').extract()
        # normalize-space(//*[@id="main"]/div/div[1]/p)
        # base_list = response.xpath('//*[@id="main"]/div/div[2]/div/div[3]/div')
        # # base_list1 = response.xpath('//*[@id="main"]/div/div[3]/button[2]').extract_first()
        #
        # for nodeList in base_list:
        #     item['rankNo'] = nodeList.xpath('normalize-space(./a/div[1]/div[1]/span/div)').extract_first()
        #     item['name'] = nodeList.xpath('normalize-space(./a/div[1]/div[3]/span/div)').extract_first()
        #     item['img'] = nodeList.xpath('normalize-space(./a/div[1]/div[2]/div[1]/div/img/@src)').extract_first()
        #     item['uri'] = 'https://opensea.io' + nodeList.xpath('normalize-space(./a/@href)').extract_first()
        #     item['volume'] = nodeList.xpath('normalize-space(./a/div[2]/div/span/div)').extract_first()
        #     item['dd24h'] = nodeList.xpath('normalize-space(./a/div[3]/div/span/div)').extract_first()
        #     item['dd7D'] = nodeList.xpath('normalize-space(./a/div[4]/div/span/div)').extract_first()
        #     item['floorPrice'] = nodeList.xpath('normalize-space(./a/div[5]/div/span/div)').extract_first()
        #     item['owners'] = nodeList.xpath('normalize-space(./a/div[7]/p)').extract_first()
        #     yield item


