import scrapy
import requests
from bs4 import BeautifulSoup


class CtitvSpider(scrapy.Spider):
    keywords = ''
    name = "gotv.ctitv.com.tw"#爬蟲名稱
    start_urls = [] #起始網址
    allowed_domains = ['gotv.ctitv.com.tw/']#允許網域

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
                'title' : title,
                'time' : time,
                'author' : author,
                'content' : content,
                'source' : self.name
            }
    def CrawlHref(self,page):#抓每一頁的網址
        google = 'https://www.google.com'
        GoogleSearch = 'https://www.google.com/search?q=site:gotv.ctitv.com.tw+' + self.keywords +'&start=' + str(page) + '0&sa=N'#ctitv網域
        r = requests.get(GoogleSearch)
        soup = BeautifulSoup(r.text,'html.parser')
        get_href = soup.select('div.kCrYT a')
        for g in get_href:
            yield google + g.get('href')

    @classmethod
    def SearchKeywords(cls):#關鍵字嵌入
        cls.keywords = str(input("輸入您要收尋的關鍵字:"))
