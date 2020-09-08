from pytrends.request import TrendReq
from googleapiclient.discovery import build
import pandas as pd
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import argparse
import scrapy
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

search_List =[] #儲存熱搜
urls_List = [] #儲存連結
keysWords_List = [] #儲存各連結關鍵字
domain_List = ["www.chinatimes.com","www.cna.com.tw","gotv.ctitv.com.tw","www.ettoday.net","news.ltn.com.tw","news.pts.org.tw","news.tvbs.com.tw"] #支持的網域列表
debug_args =""#" site:news.pts.org.tw" #除錯用額外搜尋參數


class ChinatimeNewsSpider(scrapy.Spider):
    kW = ''
    name = "www.chinatimes.com"#爬蟲名稱
    start_urls = [] #起始網址
    allowed_domains = ['www.chinatimes.com']#允許網域

    def parse(self, response):
        for n in response.css('body.content-article'):
            title = n.css('h1.article-title::text').get(default = '沒有抓到'),#獲取標題
            time = n.css('time::attr(datetime)').get(default = '沒有抓到'),#獲取文章日期、時間
            author = n.css('a::text').get(default = '沒有抓到'),#獲取作者
            for b in response.css('head'):#獲取文章內容
                html =b.css('meta::attr(content)').getall()#獲取網址
                r = requests.get(html[2])
                soup = BeautifulSoup(r.text, 'lxml')
                c = soup.select('meta')
                content = c[9]['content']
            source = '中時電子報'#文章來源
            yield{  #回傳資訊
                'keyword': self.kW,
                'title' : title,
                'time' : time,
                'author' : author,
                'content' : content,
                'source' : self.name,
                'url': self.start_urls[0]
            }

class cnaNewsSpider(scrapy.Spider):
    kW = ''
    name = "www.cna.com.tw" #爬蟲名稱
    allowed_domains = ['www.cna.com.tw'] #允許網域
    start_urls = ['https://www.cna.com.tw/news/acn/202005310121.aspx','https://www.cna.com.tw/news/firstnews/202005315002.aspx',
    'https://www.cna.com.tw/news/asoc/202005310081.aspx'] #起始網址

    def parse(self, response):
        content = ''
        for news in response.css('.centralContent'):
                title = news.css('.centralContent > h1:nth-child(2) > span:nth-child(1)::text').get(), #獲取標題
                time = news.css('.updatetime > span:nth-child(1)::text').get(), #獲取文章時間
                author = news.css('div.paragraph:nth-child(6) > p:nth-child(1)::text').re(r'（\w+）'), #獲取作者
                content_html = news.css('div.paragraph:nth-child(6)').get(), #獲取內文HTML
                content= ''.join('%s' %id for id in content_html) #將內文HTML轉換成String
                soup = BeautifulSoup(content,"lxml") #創立BS4處理
                content=soup.get_text() #使用BS4將HTML轉至文字
                content=' '.join(content.split()) #去除額外的標籤與unicode的部分
                source = '中央通訊社' #設定來源
                yield { #回傳資訊
                    'keyword': self.kW,
                    'title' : title,
                    'time' : time,
                    'author' :author,
                    'content' :content,
                    'source':self.name,
                    'url': self.start_urls[0]
                }

class CtitvSpider(scrapy.Spider):
    kW = ''
    name = "gotv.ctitv.com.tw"#爬蟲名稱
    start_urls = [] #起始網址
    allowed_domains = ['gotv.ctitv.com.tw']#允許網域

    #def start_requests(self):#爬蟲開始
        #CtitvSpider.SearchKeywords()
        #for page in range(3):#爬取3頁
            #for new in self.CrawlHref(page):#回傳網址
                #yield scrapy.Request(new, callback=self.parse)

    def parse(self, response):
        for n in response.css('body'):
            title = n.css('h1.post-title.item.fn::text').get(default = '沒有抓到')#獲取標題
            #處理GOTV特殊標題格式
            title = title.replace('\n','')#去掉title(str)多餘的\n
            title = title.replace('\t','')#去掉title(str)多餘的\t
            title = title.replace('\u3000','')#去掉title(str)多餘的\u3000
            time = n.css('time.value-title::text').get(default = '沒有抓到')#獲取文章日期、時間
            author = n.css('span.reviewer a::text').get(default = '沒有抓到')#獲取作者
            content = n.css('div.post-content.description p::text').getall()#獲取文章內容
            source = '中天GoTV'#文章來源
            yield{ #回傳資訊
                'keyword': self.kW,
                'title' : title,
                'time' : time,
                'author' : author,
                'content' : content,
                'source' : self.name
            }

class etTodayNewsSpider(scrapy.Spider):
    kW = ''
    name = "www.ettoday.net" #爬蟲名稱
    allowed_domains = ['www.ettoday.net'] #允許網域
    start_urls = ['https://www.ettoday.net/news/20200531/1726732.htm','https://www.ettoday.net/news/20200531/1726753.htm',
    'https://www.ettoday.net/news/20200531/1726719.htm'] #起始網址

    def parse(self, response):
        content = ''
        for news in response.css('.subject_article'):
                title_orginial = news.css('h1.title::text').get(), #獲取標題
                time = news.css('.date::text').get(), #獲取文章時間
                author = news.css('.story > p:nth-child(3)::text').getall(), #獲取作者
                content_html = news.css('.story').get(), #獲取內文HTML
                content= ''.join('%s' %id for id in content_html) #將內文HTML轉換成String
                title= ''.join('%s' %id for id in title_orginial) #將標題轉換成String
                soup = BeautifulSoup(content,"lxml") #創立BS4處理
                content=soup.get_text() #使用BS4將HTML轉至文字
                content=' '.join(content.split()) #去除額外的標籤與unicode的部分
                title=' '.join(title.split()) #去除額外的標籤與unicode的部分
                content = self.ContentProcess(content)
                source = ' ETtoday新聞雲' #設定來源
                yield { #回傳資訊
                    'keyword': self.kW,
                    'title' : title,
                    'time' : time,
                    'author' :author,
                    'content' :content,
                    'source':self.name,
                    'url': self.start_urls[0]
                }
    def ContentProcess(self,content):#LTN內容處理
        content = str(content)
        keep_reading_msg='請繼續往下閱讀...'
        script_remove='var ts = Math.random(); document.write(\'<scr\' + \'ipt language="JavaScript" type="text/javascript" src="https://ad.ettoday.net/ads.php?bid=lifestyle_in_news_1&rr=\'+ ts +\'"></scr\' + \'ipt>\');'
        content = content.replace(keep_reading_msg,'')
        content = content.replace(script_remove,'')
        return content

class ltnNewsSpider(scrapy.Spider):
    kW = ''
    name = "news.ltn.com.tw" #爬蟲名稱
    allowed_domains = ['news.ltn.com.tw'] #允許網域
    start_urls = ['https://news.ltn.com.tw/news/politics/breakingnews/3177607','https://news.ltn.com.tw/news/world/breakingnews/3182932',
    'https://news.ltn.com.tw/news/world/breakingnews/3182910','https://news.ltn.com.tw/news/life/breakingnews/3182911'] #起始網址

    def parse(self, response):
        content = ''
        for news in response.xpath('/html/body/div[10]'):
                title = news.css('div.whitecon:nth-child(16) > h1:nth-child(1)::text').get(), #獲取標題(ltn的whitecon:nth-child(數目),數目要+1)
                time = news.css('.time::text').get(), #獲取文章時間
                author = news.css('.text > p:nth-child(3)').re(r'〔.*〕'), #獲取作者
                content_html = news.css('.text').get(), #獲取內文HTML
                content= ''.join('%s' %id for id in content_html) #將內文HTML轉換成String
                time=''.join('%s' %id for id in time) #將時間轉換成String
                soup = BeautifulSoup(content,"lxml") #創立BS4處理
                content=soup.get_text() #使用BS4將HTML轉至文字
                content=' '.join(content.split()) #去除額外的標籤與unicode的部分
                content = self.ContentProcess(content)
                time=' '.join(time.split()) #去除額外的標籤與unicode的部分
                source = '自由時報' #設定來源
                yield { #回傳資訊
                    'keyword': self.kW,
                    'title' : title,
                    'time' : time,
                    'author' :author,
                    'content' :content,
                    'source':self.name,
                    'url': self.start_urls[0]
                }
    def ContentProcess(self,content):#LTN內容處理
        content = str(content)
        wuwan_virus_ads='相關新聞請見︰「武漢肺炎專區」請點此，更多相關訊息，帶您第一手掌握。 '
        script_remove='var disable_onead_inread = (function(){ var rang0 = [ (new Date(\'2018-06-08T00:00:00+0800\')).getTime() ,(new Date(\'2018-06-30T23:59:59+0800\')).getTime() ,{ \'focus\': true } ]; if(check_onead_mobile_inread(rang0)){ return true; } return false; })(); function check_onead_mobile_inread(rang){ var now = (new Date()).getTime(); var show_door = false; if(now>=rang[0] && now<=rang[1]){ show_door = true; var cate = rang[2]; var show_category = cate[category] ? cate[category] : false; return (show_door && show_category) ? true : false; } return false; } if(disable_onead_inread){ googletag.cmd.push(function() { googletag.defineSlot(\'/21202031/01-news-foc-P-IR2\', [[1, 1], [728, 90], [640, 360]], \'ad-inread\').addService(googletag.pubads()); googletag.enableServices(); }); $(function(){ googletag.cmd.push(function() { googletag.display(\'ad-inread\'); }); }); }else{ $(function(){ var script = document.createElement(\'script\'); script.src = "assets/js/onead_ir_mir.js"; var el = document.getElementsByTagName("script")[0]; el.parentNode.insertBefore(script, el); }); } 不用抽 不用搶 現在用APP看新聞 保證天天中獎 點我下載APP 按我看活動辦法'
        content = content.replace(wuwan_virus_ads,'')
        content = content.replace(script_remove,'')
        return content

class ptsNewsSpider(scrapy.Spider):
    kW = ''
    name = "news.pts.org.tw" #爬蟲名稱
    allowed_domains = ['news.pts.org.tw'] #允許網域
    start_urls = [] #起始網址

    def parse(self, response):
        content = ''
        for news in response.css('body'):
                title = news.css('body > div.main-info.article-main-info > div > div > div > h1::text').get(), #獲取標題
                time = news.css('body > div.main-info.article-main-info > div > div > div > div.text-muted.article-info > time::text').get(), #獲取文章時間
                author = news.css('body > div.main-info.article-main-info > div > div > div > div.text-muted.article-info > span.article-reporter.mr-2::text').getall(), #獲取作者
                content_html = news.css('body > div.container > div > div.col-lg-6 > article').get(), #獲取內文HTML
                content= ''.join('%s' %id for id in content_html) #將內文HTML轉換成String
                soup = BeautifulSoup(content,"lxml") #創立BS4處理
                content=soup.get_text() #使用BS4將HTML轉至文字
                content=' '.join(content.split()) #去除額外的標籤與unicode的部分
                yield { #回傳資訊
                    'keyword': self.kW,
                    'title' : title,
                    'time' : time,
                    'author' :author,
                    'content' :content,
                    'source':self.name,
                    'url': self.start_urls[0]
                }

class TVBSSpider(scrapy.Spider):
    kW = ''
    name = "news.tvbs.com.tw"#爬蟲名稱
    allowed_domains = ['news.tvbs.com.tw']#允許網域
    start_urls = [] #起始網址
    ###拒絕網域
    rules = (
        Rule(LinkExtractor(deny=('news/searchresult/*')), callback = 'parse'))

    def parse(self, response):
        for n in response.css('body'):
            title = n.css('h1::text').get(default = '沒有抓到')#獲取標題
            #處理TVBS特殊標題格式
            title = title.replace('\u3000','')#去掉title(str)多餘的\u3000
            time = n.css('div.icon_time.time.leftBox2::text').get(default = '沒有抓到')#獲取文章日期、時間
            author = n.css('h4 > a::text').get(default = '沒有作者')#獲取作者
            content = n.css('div.h7.margin_b20 > p::text').getall() + n.css('div.h7.margin_b20::text').getall()#獲取文章內容
            content = self.ContentProcess(content)#文章內容處理
            source = 'TVBS'#文章來源
            yield{ #回傳資訊
                'keyword': self.kW,
                'title' : title,
                'time' : time,
                'author' : author,
                'content' : content,
                'source' : self.name,
                'url': self.start_urls[0]
            }
    def ContentProcess(self,content):#TVBS專屬內文處理
        content = str(content)
        content = content.replace('\\xa0','')
        content = content.replace('\\n','')
        content = content.replace('\\t','')
        content = content.replace('\\r','')
        #因疫情文章做處理"
        content = content.replace('因應新冠肺炎疫情，疾管署持續加強疫情監測與邊境管制措施，','')
        content = content.replace('並','')
        content = content.replace('，同時','')
        content = content.replace('，以利及時診斷及通報。','')
        content = content.replace('邀請世界各角落的你','')
        content = content.replace('加入Facebook社團【','')
        content = content.replace('】','')
        content = content.replace('','')
        return content

def process_command():
    parser = argparse.ArgumentParser(description='執行資料爬蟲')
    parser.add_argument('--gibmode','-gm',type=str,default='auto',help='資料抓取模式 \n 參數為Auto或a將從 Google搜尋趨勢 最近前20名的關鍵字進行抓取 \n Manual或m並接上 -kw 手動關鍵字 進行手動輸入搜尋。')
    parser.add_argument('--keyword','-kw',type=str,default='',help='手動搜尋時的關鍵字')
    return parser.parse_args()

def startSpider():
    global urls_List
    process = CrawlerProcess(settings={
    "FEEDS": {
        "news_article.json": {"format": "json",'encoding': 'utf8',
        'store_empty': False,'fields': None,
        'indent': 4,},
    },"DOWNLOAD_DELAY":2,
})
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
        gQuery = google_query(keyWord,api_key,cse_id,num = 5) #num為抓取數
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