import scrapy
import requests
from bs4 import BeautifulSoup


class CtitvSpider(scrapy.Spider):
    name = "gotv.ctitv.com.tw"#爬蟲名稱
    allowed_domains = ['gotv.ctitv.com.tw/']#允許網域
    def start_requests(self):#更換網址
        for a in self.keywordsSearch():
            yield scrapy.Request(a)
    def parse(self, response):
        for n in response.css('body'):
            title = n.css('h1.post-title.item.fn::text').get(default = '沒有抓到')#獲取標題
            #處理GOTV特殊標題格式
            title = title.replace('\n','')#去掉title(str)多餘的\n
            title = title.replace('\t','')#去掉title(str)多餘的\t
            time = n.css('time.value-title::text').get(default = '沒有抓到')#獲取文章日期、時間
            author = n.css('span.reviewer a::text').get(default = '沒有抓到')#獲取作者
            content = n.css('div.post-content.description p::text').getall()#獲取文章內容
            source = '中天GoTV'#文章來源
            yield{ #回傳資訊
                'title' : title,
                'time' : time,
                'author' : author,
                'content' : content,
                'source' : source
            }
    def SearchHref(self,keywords):#抓標題網址
        google = 'https://www.google.com'
        GoogleSearch = 'https://www.google.com/search?q=site:gotv.ctitv.com.tw%20'#ctitv網域
        url = GoogleSearch + keywords
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        get_href = soup.select('div.kCrYT a')
        for g in get_href:
            yield google + g.get('href')

    def keywordsSearch(self):#收尋關鍵字
        keywords = str(input("輸入您要收尋的關鍵字:"))
        keywords_url = self.SearchHref(keywords)#進入SearchHref()方法
        return keywords_url   