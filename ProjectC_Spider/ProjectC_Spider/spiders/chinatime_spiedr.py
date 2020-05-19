import scrapy
import requests
from bs4 import BeautifulSoup

class ChinatimeNewsSpider(scrapy.Spider):
    name = "Chinatime.spider"#爬蟲名稱
    allowed_domains = ['www.chinatimes.com/']#允許網域
    start_urls = ['https://www.chinatimes.com/realtimenews/20200516002044-260410?chdtv']#起始網址
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
                'source' : source
            }
            