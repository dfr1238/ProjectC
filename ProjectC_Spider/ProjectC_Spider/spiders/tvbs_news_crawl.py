import scrapy
import requests
from bs4 import BeautifulSoup
from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class TVBSSpider(scrapy.Spider):
    keywords = ''
    name = "news.tvbs.com.tw"#爬蟲名稱
    allowed_domains = ['news.tvbs.com.tw/']#允許網域
    start_urls = [] #起始網址
    ###拒絕網域
    rules = (
        Rule(LinkExtractor(deny=('news/searchresult/*')), callback = 'parse'))

    #def start_requests(self):#爬蟲開始
        #TVBSSpider.SearchKeywords()
        #for page in range(3):
            #for new in self.CrawlHref(page):
                #yield scrapy.Request(new, callback=self.parse)

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
                'title' : title,
                'time' : time,
                'author' : author,
                'content' : content,
                'source' : self.name
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

    def CrawlHref(self,page):#抓每一頁的網址
        google = 'https://www.google.com'
        GoogleSearch = 'https://www.google.com/search?q=site:news.tvbs.com.tw+' + self.keywords + '&ie=UTF-8&start='+ str(page) + '0&sa=N'#TVBS網域
        r = requests.get(GoogleSearch)
        soup = BeautifulSoup(r.text,'html.parser')
        get_href = soup.select('div.kCrYT a')
        for g in get_href:
            yield google + g.get('href')
    
    @classmethod
    def SearchKeywords(cls):
        cls.keywords = str(input("輸入您要收尋的關鍵字:"))
    


