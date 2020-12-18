from pytrends.request import TrendReq
from ProjectC_Spider.spiders.mega_crawl import ChinatimeNewsSpider
from ProjectC_Spider.spiders.mega_crawl import cnaNewsSpider
from ProjectC_Spider.spiders.mega_crawl import CtitvSpider
from ProjectC_Spider.spiders.mega_crawl import etTodayNewsSpider
from ProjectC_Spider.spiders.mega_crawl import ltnNewsSpider
from ProjectC_Spider.spiders.mega_crawl import ptsNewsSpider
from ProjectC_Spider.spiders.mega_crawl import TVBSSpider
from googleapiclient.discovery import build
import pandas as pd
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess, Crawler
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
import argparse
import scrapy
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from protego import Protego

search_List =[] #儲存熱搜
urls_List = [] #儲存連結
keysWords_List = [] #儲存各連結關鍵字
domain_List = ["www.chinatimes.com","www.cna.com.tw","gotv.ctitv.com.tw","www.ettoday.net","news.ltn.com.tw","news.pts.org.tw","news.tvbs.com.tw"] #支持的網域列表
debug_args =""#" site:news.pts.org.tw" #除錯用額外搜尋參數

def process_command():
    parser = argparse.ArgumentParser(description='執行資料爬蟲')
    parser.add_argument('--gibmode','-gm',type=str,default='auto',help='資料抓取模式 \n 參數為Auto或a將從 Google搜尋趨勢 最近前20名的關鍵字進行抓取 \n Manual或m並接上 -kw 手動關鍵字 進行手動輸入搜尋。')
    parser.add_argument('--keyword','-kw',type=str,default='',help='手動搜尋時的關鍵字')
    return parser.parse_args()

def startSpider():
    global urls_List
    process = CrawlerProcess(get_project_settings())

    for Url,keyWord in zip(urls_List,keysWords_List):
        Urls = [Url]
        if urlparse(Url).netloc == "www.chinatimes.com":
            process.crawl(ChinatimeNewsSpider,start_urls=Urls,kW=keyWord)
        if urlparse(Url).netloc == "www.cna.com.tw":
            process.crawl(cnaNewsSpider,start_urls=Urls,kW=keyWord)
        if urlparse(Url).netloc == "gotv.ctitv.com.tw":
            process.crawl(CtitvSpider,start_urls=Urls,kW=keyWord)
        if urlparse(Url).netloc == "www.ettoday.net":
            process.crawl(etTodayNewsSpider,start_urls=Urls,kW=keyWord)
        if urlparse(Url).netloc == "news.ltn.com.tw":
            process.crawl(ltnNewsSpider,start_urls=Urls,kW=keyWord)
        if urlparse(Url).netloc == "news.pts.org.tw":
            process.crawl(ptsNewsSpider,start_urls=Urls,kW=keyWord)
        if urlparse(Url).netloc == "news.tvbs.com.tw":
            process.crawl(TVBSSpider,start_urls=Urls,kW=keyWord)
    process.start()

def googleSearch():
    global urls_List
    global keysWords_List
    print('Start Search On Google Search...Listing Search Items...')
    print(search_List)
    api_key = "AIzaSyBLbpitcRlCegFlIfE6GKNYrX9jeVBcmIY" #Google Search Console API Key
    cse_id = "21a2dbd3070dbb894" #Google 程式化引擎搜尋ID

    def google_query(query, api_key,cse_id, **kwargs):
        query_service = build("customsearch", 
                          "v1", 
                          developerKey=api_key
                          )  
        query_results = query_service.cse().list(q=query,    # Query
                                             cx=cse_id,  # CSE ID
                                             **kwargs    
                                             ).execute()
        if 'items' in query_results.keys():
            return query_results['items']
        else:
            return None                
    
    for keyWord in search_List:
        kw = "".join(keyWord)
        keyWord[0]=kw+debug_args
        print(keyWord)
        gQuery = google_query(keyWord,api_key,cse_id,num = 10) #num為抓取數
        print(type(gQuery))
        if gQuery is None:
            continue
        my_results = gQuery
        for result in my_results:
            urls_List.append(result['link'])
            keysWords_List.append(kw)
            print(result['link'])
    
def gibGoogleTrends():
    global search_List
    pytrend = TrendReq(hl='zh-TW') #建立與Google Trend連線
    dailyTrend_df = pytrend.trending_searches(pn='taiwan') #列出每日流行趨勢搜尋
    search_List  = dailyTrend_df.values.tolist()
    print('gib from Google Trends Finish.')

def main():
    
    if(args.gibmode.lower() == 'auto' or  args.gibmode.lower() == 'a'):
        print('using auto gib mode,trying gib from Google Trends...')
        gibGoogleTrends()
        googleSearch()
        startSpider()
    if(args.gibmode.lower() == 'manual' or args.gibmode.lower() == 'm'):
        print('using maunal gib mode,check keyword...')
        if(args.keyword == ''):
            print('please enter keyword with -kw <keyword>')
        else:
            global search_List
            argskw = [args.keyword]
            print('Keyword:'+args.keyword)
            search_List.append(argskw)
            googleSearch()
            startSpider()

if __name__ == "__main__":
    args = process_command() #GIB ༼ つ ◕_◕ ༽つ
    main()