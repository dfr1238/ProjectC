import scrapy
import requests
from bs4 import BeautifulSoup

class ChinatimeNewsSpider(scrapy.Spider):
    keywords = ''
    name = "www.chinatimes.com"#爬蟲名稱
    start_urls = [] #起始網址
    allowed_domains = ['www.chinatimes.com/']#允許網域

    #def start_requests(self):#更換網址
        #ChinatimeNewsSpider.SearchKeywords()
        #for page in range(3):#爬取3頁
            #for new in self.CrawlHref(page):
                #yield scrapy.Request(new, callback=self.parse)
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
                'title' : title,
                'time' : time,
                'author' : author,
                'content' : content,
                'source' : self.name
            }
    def CrawlHref(self,page):#抓每一頁的網址
        google = 'https://www.google.com'
        GoogleSearch = 'https://www.google.com/search?q=site:www.chinatimes.com+' + self.keywords +'&start=' + str(page) + '0&sa=N'#chinatime網域
        r = requests.get(GoogleSearch)
        soup = BeautifulSoup(r.text,'html.parser')
        get_href = soup.select('div.kCrYT a')
        for g in get_href:
            yield google + g.get('href')

    @classmethod
    def SearchKeywords(cls):#關鍵字嵌入
        cls.keywords = str(input("輸入您要收尋的關鍵字:"))
