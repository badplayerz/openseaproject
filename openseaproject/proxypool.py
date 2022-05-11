import math
import random
import threading
import logging
import time
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

class FetchProxy(threading.Thread):
    def __init__(self, ppp, uri):
        threading.Thread.__init__(self)
        self.pp = ppp
        self.uri = uri
        # print('self.num = '+ str(self.num))

    """
    收集代理信息并赋值给调用者
    """
    def run(self):
        self.pp.update(getattr(self, 'fetch_proxy_from_'+self.uri)())

    def fetch_proxy_from_ip3336(self):
        proxys = {}
        url = 'http://www.ip3366.net/free/?stype=1&page='
        try:
            for i in range(1, 6):
                soup = self.get_soup(url + str(i))

                trs = soup.find("div", attrs={"id": "list"}).table.find_all("tr")
                for i, tr in enumerate(trs):
                    if 0 == i:
                        continue
                    tds = tr.find_all("td")
                    ip = tds[0].string.strip().encode('utf-8')
                    port = tds[1].string.strip().encode('utf-8')
                    proxy = ''.join(['http://', ip.decode('utf-8'), ':', port.decode('utf-8')])
                    proxys[proxy] = False
        except Exception as e:
            logger.error('Failed to fetch_proxy_from_ip3336. Exception[%s]', e)
        return proxys

    def fetch_proxy_from_kxdaili(self):
        proxys = {}
        url = 'http://www.kxdaili.com/dailiip/1/%d.html'
        try:
            for i in range(1, 10):
                soup = self.get_soup(url % i)
                print(url % i)
                trs = soup.find("table", attrs={"class": "active"}).find_all("tr")
                for i, tr in enumerate(trs):
                    if 0 == i:
                        continue
                    tds = tr.find_all("td")
                    ip = tds[0].string.strip().encode('utf-8')
                    port = tds[1].string.strip().encode('utf-8')
                    proxy = ''.join(['http://', ip.decode('utf-8'), ':', port.decode('utf-8')])
                    proxys[proxy] = False
        except Exception as e:
            logger.error('Failed to fetch_proxy_from_kxdaili. Exception[%s]', e)

        return proxys

    def get_soup(self, url):

        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        timeout = 30
        while True:
            try:

                html_doc = requests.get(url,headers=headers ,timeout=timeout)
                break
            except:
                logger.info("Fetch proxy from {} fail, will try later.".format(url))
                time.sleep(120)

        soup = BeautifulSoup(html_doc.text)

        return soup





class VaildateProxy(threading.Thread):
    def __init__(self, _autoproxy,  _proxy_list_dic):
        threading.Thread.__init__(self)
        self.autoproxy = _autoproxy
        self.proxy_list_dic = _proxy_list_dic

    def run(self):
        for _proxy,_valid in self.proxy_list_dic.items():
            if(self.check_proxy(_proxy)):
                self.autoproxy.proxys[_proxy] = True
                self.autoproxy.append_true_proxy(_proxy)


    def check_proxy(self,_proxy):
        ip = _proxy[7:]
        ips = {"http": "http://" + ip, "https": "https://" + ip}
        try:
            response = requests.get(self.autoproxy.test_check_uri, proxies=ips, timeout=4)
            if response.status_code == 200 and 'http://httpbin.org/get' in response.text:
                return True

            return False
        except:
            return False



class autoproxy(object):

    def __init__(self):
        self.true_proxy = []
        self.proxys = {}
        self.test_threads_nums = 20
        self.test_check_uri = 'http://httpbin.org/get'

        self.get_proxy_pool() #获取ip代理池赋值给self.proxys
        self.test_proxy_pool(self.proxys)

        print(self.true_proxy)

    def get_proxy_pool(self,):
        uris = ['ip3336', 'kxdaili']
        threads = []
        for t in uris:
            fp = FetchProxy(self.proxys, t)
            threads.append(fp)
            fp.start()

        for tj in threads:
            tj.join()

    def test_proxy_pool(self,_proxys):
        proxy_list = list(_proxys.items())
        threads = []
        i = math.ceil(len(proxy_list) / self.test_threads_nums)  # 平均分每个线程的代理ip数量
        for n in range(self.test_threads_nums):
            proxy_list_dic = {k: v for k, v in proxy_list[n * i:(n + 1) * i]}
            t = VaildateProxy(self, proxy_list_dic)
            threads.append(t)
            t.start()

        for n in threads:
            n.join()

    """
    添加验证过可用代理
    """
    def append_true_proxy(self,_proxy):
        if _proxy not in self.true_proxy:
            self.true_proxy.append(_proxy)

if __name__ == "__main__":
    print('main')

    autoproxy()

