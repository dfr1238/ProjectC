import scrapy
from bs4 import BeautifulSoup
class cnaNewsSpider(scrapy.Spider):
    name = "www.cna.com.tw" #爬蟲名稱
    allowed_domains = ['www.cna.com.tw/'] #允許網域
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
                    'title' : title,
                    'time' : time,
                    'author' :author,
                    'content' :content,
                    'source':source,
                }