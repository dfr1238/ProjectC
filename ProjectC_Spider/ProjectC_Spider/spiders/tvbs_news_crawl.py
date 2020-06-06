import scrapy
import requests
from bs4 import BeautifulSoup


class TVBSSpider(scrapy.Spider):
    name = "news.tvbs.com.tw"#爬蟲名稱
    allowed_domains = ['news.tvbs.com.tw/']#允許網域
    def start_requests(self):#更換網址
        for a in self.keywordsSearch():
            yield scrapy.Request(a)
    def parse(self, response):
        #content = ''
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
                'source' : source
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
    def SearchHref(self,keywords):#抓標題網址
        google = 'https://www.google.com'
        GoogleSearch = 'https://www.google.com/search?q=site:news.tvbs.com.tw%20'#tvbs網域
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