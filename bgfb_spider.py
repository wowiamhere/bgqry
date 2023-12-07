from pathlib import Path
import scrapy
import chompjs
import pprint
import hashlib
import random

CURRENT_HASH = ',,,,,,,,,'
CURRENT_POST = ''

CUSTOM_HEADER_NAMES = [ 'opera_desktop_linux' ]

CUSTOM_HEADERS = {
        'opera_desktop_linux': {
            'scheme':'https',
            'method':'GET',
            'path':'/centralcastinglosangeles',
            'authority':'www.facebook.com',
            'sec-ch-ua':'"Opera";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Linux"',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'sec-fetch-site':'none',
            'sec-fetch-mode':'navigate',
            'sec-fetch-user':'?1',
            'sec-fetch-dest':'document',
            'accept-encoding':'gzip, deflate',
            'accept-language':'en-US,en;q=0.9'
            },
        'chrome_desktop_linux': {
            'authority':'www.facebook.com',
            'method':'GET',
            'path':'/centralcastinglosangeles/',
            'scheme':'https',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding':'gzip, deflate',
            'accept-language':'en-US,en;q=0.9',
            'dnt':'1',
            'sec-ch-ua':'"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Linux"',
            'sec-fetch-dest':'document',
            'sec-fetch-mode':'navigate',
            'sec-fetch-site':'none',
            'sec-fetch-user':'?1',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        },
        'micrsft_edge_desktop_mac':{
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding':'gzip, deflate',
            'accept-language':'en-US,en;q=0.9',
            'sec-ch-ua':'"Not A;Brand";v="99", "Chromium";v="119", "Microsoft Edge";v="119"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"macOS"',
            'sec-fetch-dest':'document',
            'sec-fetch-mode':'navigate',
            'sec-fetch-site':'none',
            'sec-fetch-user':'?1',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/604.1 Edg/119.0.100.0'
        },
        'chrome_os':{
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding':'gzip, deflate',
            'accept-language':'en-US,en;q=0.9',
            'sec-ch-Ua':'"Not A;Brand";v="99", "Chromium";v="119", "Google Chrome";v="119"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Chrome OS"',
            'sec-fetch-dest':'document',
            'sec-fetch-mode':'navigate',
            'sec-fetch-site':'none',
            'sec-fetch-user':'?1',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (X11; CrOS x86_64 10066.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        },
        'chrome_win':{
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding':'gzip, deflate',
            'accept-language':'en-US,en;q=0.9',
            'cache-control':'no-cache',
            'dnt':'1',
            'pragma':'no-cache',
            'sec-ch-ua':'"Not A;Brand";v="99", "Chromium";v="119", "Google Chrome";v="119"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':'"Windows"',
            'sec-fetch-dest':'document',
            'sec-fetch-mode':'navigate',
            'sec-fetch-site':'none',
            'sec-fetch-user':'?1',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }}

proxy_user = ''
proxy_p = ''
proxy_port = ''
proxy_ip = ''
proxy = "https://{}:{}:@{}:{}".format( proxy_user, proxy_p, proxy_ip, proxy_port )

class bgfb(scrapy.Spider):
    name = "bgqrycls"
    
    custom_settings = {
            'BOT_NAME':'bgqry',
            'MAIL_FROM':'',
            'USER_AGENT':'',
            'DEFAULT_REQUEST_HEADERS':'',
            'DOWNLOADER_MIDDLEWARES':{
                'bgfb_spider.CustomUserAgentMiddleware': 350,
                'bgfb_spider.CustomHeadersMiddleware': 350,
                },
            }


    this_hash = ''

    def start_requests(self):
        urls = [ '' ]
        for url in urls:
            yield scrapy.Request( url=url, meta={ 'dont_merge_cookies':True }, callback=self.parse )

        
    def parse(self, response):
        global CURRENT_HASH
        global CURRENT_POST
        pattern = r'"message":{"text"[.]*:"[\W\da-zA-Z]*"}'
        text = response.css('script::text').re_first( pattern )

        try:
            data = chompjs.chompjs.parse_js_object( text )
            self.this_hash = hashlib.sha224( data['text'].encode('utf-8') ).hexdigest()
            CURRENT_HASH = self.this_hash
            CURRENT_POST = data['text']
        except Exception as e:
            print('*************TEXT ERROR!!!!!!!!!!', e)

class CustomUserAgentMiddleware:

    def __init__(self, ua_strings):
        self.ua_strings = ua_strings

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        #spider = super().from_crawler(crawler, *args, **kwargs)
        return cls 


class CustomHeadersMiddleware:
    def __init__(self, hdrs):
        self.hdrs = hdrs

    @classmethod
    def from_crawler(cls, crawler):
        hdrs_ar = random.choice( CUSTOM_HEADER_NAMES )
        hdrs = scrapy.http.headers.Headers( CUSTOM_HEADERS[ hdrs_ar ] )
        crawler.spider.custom_settings['USER-AGENT'] = hdrs['user-agent']
        return cls(hdrs)

    def process_request(self, request, spider):
        request.headers = self.hdrs
        request.meta['proxy'] = proxy


