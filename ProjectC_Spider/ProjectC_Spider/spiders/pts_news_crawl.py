import scrapy
from bs4 import BeautifulSoup
class ptsNewsSpider(scrapy.Spider):
    name = "news.pts.org.tw" #爬蟲名稱
    allowed_domains = ['news.pts.org.tw/'] #允許網域
    start_urls = ['https://news.pts.org.tw/article/473677','https://news.pts.org.tw/article/480307'] #起始網址

    def parse(self, response):
        content = ''
        for news in response.css('body.newscont-page'):
                title = news.css('.article-title::text').get(), #獲取標題
                time = news.css('div.hidden-sm:nth-child(1) > h2:nth-child(1)::text').get(), #獲取文章時間
                author = news.css('div.hidden-sm:nth-child(1) > div:nth-child(2)::text').getall(), #獲取作者
                content_html = news.css('.article_content').get(), #獲取內文HTML
                content= ''.join('%s' %id for id in content_html) #將內文HTML轉換成String
                soup = BeautifulSoup(content,"lxml") #創立BS4處理
                content=soup.get_text() #使用BS4將HTML轉至文字
                content=' '.join(content.split()) #去除額外的標籤與unicode的部分
                source = '公視新聞網' #設定來源
                yield { #回傳資訊
                    'title' : title,
                    'time' : time,
                    'author' :author,
                    'content' :content,
                    'source':source,
                }