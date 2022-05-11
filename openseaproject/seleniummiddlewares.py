# Define here the models for your spider middleware
# selenium中间件
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy.http
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.utils.project import get_project_settings
import logging

logger = logging.getLogger('seleniummidd')

class OpenseaprojectSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.

        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).

        pass

class OpenseaprojectDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    PAGEMAX = 0
    cSettings = None

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"')
        chrome_options.add_argument('--window-size=1920,5000')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                      get: () => undefined
                    })
                  """
        })

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):

        logger.debug('request')
        print('proxy++++',request.meta['proxy'])
        pageNum = request.meta.get('page',0)

        if pageNum > 0:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id=\"main\"]/div/div[3]/button[2]"))).click()
            time.sleep(2)

        else:
            self.driver.get(request.url)
            time.sleep(3)
            print('99999' + str(pageNum))


        # self.driver.execute_script('window.scrollTo(0,10000)')

        # for x in range(1, 11, 2):
        #     height = float(x) / 10
        #     js = "document.documentElement.scrollTop = document.documentElement.scrollHeight * %f" % height
        #     self.driver.execute_script(js)
        #     time.sleep(0.2)

        # time.sleep(3)
        # js = "window.scrollTo(0,document.body.scrollHeight)"
        # self.driver.execute_script(js)
        # time.sleep(3)


        html = self.driver.page_source

        self.closecSpiner(pageNum)

        return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',request=request)


    # 自定义关闭方法，判断最后爬取次数与settings设置最大爬取次数相同则关闭浏览器driver
    # 需要from scrapy.utils.project import get_project_settings
    # 需要定义全局变量cSettings、PAGEMAX
    def closecSpiner(self, pageNum):
        if self.cSettings is None:
            self.cSettings = get_project_settings()
            self.PAGEMAX = self.cSettings.get('MAX_PAGE_NUM')
        if self.PAGEMAX != 0 and pageNum == self.PAGEMAX-1:
            self.driver.quit()


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        logger.debug('response')
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
