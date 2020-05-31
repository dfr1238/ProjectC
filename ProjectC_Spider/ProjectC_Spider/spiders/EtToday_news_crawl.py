import scrapy
from bs4 import BeautifulSoup
class etTodayNewsSpider(scrapy.Spider):
    name = "www.ettoday.net" #爬蟲名稱
    allowed_domains = ['www.ettoday.net/'] #允許網域
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
                    'title' : title,
                    'time' : time,
                    'author' :author,
                    'content' :content,
                    'source':source,
                }
    def ContentProcess(self,content):#LTN內容處理
        content = str(content)
        keep_reading_msg='請繼續往下閱讀...'
        script_remove='var ts = Math.random(); document.write(\'<scr\' + \'ipt language="JavaScript" type="text/javascript" src="https://ad.ettoday.net/ads.php?bid=lifestyle_in_news_1&rr=\'+ ts +\'"></scr\' + \'ipt>\');'
        content = content.replace(keep_reading_msg,'')
        content = content.replace(script_remove,'')
        return content