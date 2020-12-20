import scrapy
import requests
from bs4 import BeautifulSoup
from scrapy.exceptions import CloseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import VscodeSshScrapyTestItem

class ChinatimeNewsSpider(scrapy.Spider):
    kW = ''
    name = "www.chinatimes.com"#爬蟲名稱
    start_urls = [] #起始網址
    allowed_domains = ['www.chinatimes.com']#允許網域

    def parse(self, response):
        items = VscodeSshScrapyTestItem()#匯入items
        for n in response.css('div.article-wrapper'):
            items['title'] = n.css('h1.article-title::text').get(default = '沒有抓到'),#獲取標題
            items['time'] = n.css('div.meta-info > time::attr(datetime)').get(default = '沒有抓到'),#獲取文章日期、時間
            items['author'] = n.css('div.author > a::text').get(default = '沒有抓到'),#獲取作者
            content_html = n.css('div.article-body').get(), #獲取內文HTML
            remove_parts = n.css('div.promote-word > a::text').getall(), #獲取多餘內容
            remove_parts_2 = n.css('div.article-hash-tag > span.hash-tag > a::text').getall(), #獲取文章Hash-tag
            remove_parts = ' '.join(remove_parts[0]) #將多餘內容轉換成字串
            remove_parts_2 = ' #'.join(remove_parts_2[0]) #將Hash-tag轉換成字串
            remove_parts_2 = '#'+remove_parts_2 #補正字串
            content= ''.join('%s' %id for id in content_html) #將內文HTML轉換成String
            soup = BeautifulSoup(content,"lxml") #創立BS4處理
            content=soup.get_text() #使用BS4將HTML轉至文字
            content=' '.join(content.split()) #去除額外的標籤與unicode的部分
            content=content.replace(remove_parts,'') #從內文移除額外內容
            items['content']=content.replace(remove_parts_2,'') #從內文移除Hash-tag
            items['source'] = '中時電子報'#文章來源
            items['keyword'] = self.kW
            items['url'] = self.start_urls[0]
            yield(items)  #回傳資訊

class cnaNewsSpider(scrapy.Spider):
    kW = ''
    name = "www.cna.com.tw" #爬蟲名稱
    allowed_domains = ['www.cna.com.tw'] #允許網域
    start_urls = [] #起始網址

    def parse(self, response):
        items = VscodeSshScrapyTestItem()#匯入items
        content = ''
        for news in response.css('.centralContent'):
                items['title'] = news.css('.centralContent > h1 > span::text').get(), #獲取標題
                items['time'] = news.css('.updatetime > span:nth-child(1)::text').get(), #獲取文章時間
                items['author'] = news.css('div.paragraph:nth-child(6) > p:nth-child(1)::text').re(r'（\w+）'), #獲取作者
                content_html = news.css('div.paragraph').get(), #獲取內文HTML
                remove_parts = news.css('div.paragraph > .moreArticle').get() #獲取更多內容HTML
                remove_parts = ''.join(remove_parts)
                #print(remove_parts)
                content= ''.join('%s' %id for id in content_html) #將內文HTML轉換成String
                content=content.replace(remove_parts,'') #從內文HTML移除更多內容
                soup = BeautifulSoup(content,"lxml") #創立BS4處理
                content=soup.get_text() #使用BS4將HTML轉至文字
                items['content']=' '.join(content.split()) #去除額外的標籤與unicode的部分
                items['source'] = '中央通訊社' #設定來源
                items['keyword'] = self.kW
                items['url'] = self.start_urls[0]
                yield (items) #回傳資訊


class CtitvSpider(scrapy.Spider):
    kW = ''
    name = "gotv.ctitv.com.tw"#爬蟲名稱
    start_urls = ['https://gotv.ctitv.com.tw/2020/10/1531205.htm'] #起始網址
    allowed_domains = ['gotv.ctitv.com.tw']#允許網域

    def parse(self, response):
        items = VscodeSshScrapyTestItem()#匯入items
        for n in response.css('body'):
            title = n.css('h1.post-title.item.fn::text').get(default = '沒有抓到')#獲取標題
            #處理GOTV特殊標題格式
            title = title.replace('\n','')#去掉title(str)多餘的\n
            title = title.replace('\t','')#去掉title(str)多餘的\t
            items['title'] = title.replace('\u3000','')#去掉title(str)多餘的\u3000
            items['time'] = n.css('time.value-title::text').get(default = '沒有抓到')#獲取文章日期、時間
            items['author'] = n.css('span.reviewer a::text').get(default = '沒有抓到')#獲取作者
            items['content'] = n.css('div.post-content.description p::text').getall()#獲取文章內容
            items['source'] = '中天GoTV'#文章來源
            items['keyword'] = self.kW
            items['url'] = self.start_urls[0]
            yield(items) #回傳資訊


class etTodayNewsSpider(scrapy.Spider):
    kW = ''
    name = "www.ettoday.net" #爬蟲名稱
    allowed_domains = ['www.ettoday.net'] #允許網域
    start_urls = ['https://www.ettoday.net/news/20201011/1829226.htm'] #起始網址

    def parse(self, response):
        items = VscodeSshScrapyTestItem()#匯入items
        content = ''
        for news in response.css('div.c1'):
                title_orginial = news.css('h1.title::text').get(), #獲取標題
                items['time'] = news.css('time::attr(datetime)').get(), #獲取文章時間
                items['author'] = news.css('.story > p:nth-child(2)::text').getall(), #獲取作者
                content_html = news.css('.story').get(), #獲取內文HTML
                content= ''.join('%s' %id for id in content_html) #將內文HTML轉換成String
                title= ''.join('%s' %id for id in title_orginial) #將標題轉換成String
                soup = BeautifulSoup(content,"lxml") #創立BS4處理
                content=soup.get_text() #使用BS4將HTML轉至文字
                content=' '.join(content.split()) #去除額外的標籤與unicode的部分
                items['title']=' '.join(title.split()) #去除額外的標籤與unicode的部分
                items['content'] = self.ContentProcess(content)
                items['source'] = ' ETtoday新聞雲' #設定來源
                items['keyword'] = self.kW
                items['url'] = self.start_urls[0]
                yield(items) #回傳資訊                
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
    start_urls = [''] #起始網址
    ###拒絕網域
    rules = (
        Rule(LinkExtractor(deny=('topic/*')), callback = 'parse'))

    def parse(self, response):
        items = VscodeSshScrapyTestItem()#匯入items
        content = ''
        for news in response.xpath('/html/body/div[10]'):
                items['title'] = news.css('div.whitecon:nth-child(16) > h1:nth-child(1)::text').get(), #獲取標題(ltn的whitecon:nth-child(數目),數目要+1)
                time = news.css('.time::text').get(), #獲取文章時間
                items['author'] = news.css('.text > p:nth-child(3)').re(r'〔.*〕'), #獲取作者
                content_html = news.css('.text').get(), #獲取內文HTML
                content= ''.join('%s' %id for id in content_html) #將內文HTML轉換成String
                time=''.join('%s' %id for id in time) #將時間轉換成String
                soup = BeautifulSoup(content,"lxml") #創立BS4處理
                content=soup.get_text() #使用BS4將HTML轉至文字
                content=' '.join(content.split()) #去除額外的標籤與unicode的部分
                items['content'] = self.ContentProcess(content)
                items['time'] =' '.join(time.split()) #去除額外的標籤與unicode的部分
                items['source'] = '自由時報' #設定來源
                items['keyword'] = self.kW
                items['url'] = self.start_urls[0]
                yield (items) #回傳資訊
    def ContentProcess(self,content):#LTN內容處理
        content = str(content)
        wuwan_virus_ads='相關新聞請見︰「武漢肺炎專區」請點此，更多相關訊息，帶您第一手掌握。 '
        script_remove='var disable_onead_inread = (function(){ var rang0 = [ (new Date(\'2018-06-08T00:00:00+0800\')).getTime() ,(new Date(\'2018-06-30T23:59:59+0800\')).getTime() ,{ \'focus\': true } ]; if(check_onead_mobile_inread(rang0)){ return true; } return false; })(); function check_onead_mobile_inread(rang){ var now = (new Date()).getTime(); var show_door = false; if(now>=rang[0] && now<=rang[1]){ show_door = true; var cate = rang[2]; var show_category = cate[category] ? cate[category] : false; return (show_door && show_category) ? true : false; } return false; } if(disable_onead_inread){ googletag.cmd.push(function() { googletag.defineSlot(\'/21202031/01-news-foc-P-IR2\', [[1, 1], [728, 90], [640, 360]], \'ad-inread\').addService(googletag.pubads()); googletag.enableServices(); }); $(function(){ googletag.cmd.push(function() { googletag.display(\'ad-inread\'); }); }); }else{ $(function(){ var script = document.createElement(\'script\'); script.src = "assets/js/onead_ir_mir.js"; var el = document.getElementsByTagName("script")[0]; el.parentNode.insertBefore(script, el); }); } 不用抽 不用搶 現在用APP看新聞 保證天天中獎 點我下載APP 按我看活動辦法'
        app_ads=' 不用抽 不用搶 現在用APP看新聞 保證天天中獎 點我下載APP 按我看活動辦法'
        content = content.replace(wuwan_virus_ads,'')
        content = content.replace(script_remove,'')
        content = content.replace(app_ads,'')
        return content

class ptsNewsSpider(scrapy.Spider):
    kW = ''
    name = "news.pts.org.tw" #爬蟲名稱
    allowed_domains = ['news.pts.org.tw'] #允許網域
    start_urls = [''] #起始網址

    def parse(self, response):
        items = VscodeSshScrapyTestItem()#匯入items
        content = ''
        for news in response.css('body'):
                items['title'] = news.css('body > div.main-info.article-main-info > div > div > div > h1::text').get(), #獲取標題
                items['time'] = news.css('body > div.main-info.article-main-info > div > div > div > div.text-muted.article-info > time::text').get(), #獲取文章時間
                items['author'] = news.css('body > div.main-info.article-main-info > div > div > div > div.text-muted.article-info > span.article-reporter.mr-2::text').getall(), #獲取作者
                content_html = news.css('body > div.container > div > div.col-lg-6 > article').get(), #獲取內文HTML
                content= ''.join('%s' %id for id in content_html) #將內文HTML轉換成String
                soup = BeautifulSoup(content,"lxml") #創立BS4處理
                content=soup.get_text() #使用BS4將HTML轉至文字
                items['content'] =' '.join(content.split()) #去除額外的標籤與unicode的部分
                items['source'] = self.name
                items['keyword'] = self.kW
                items['url'] = self.start_urls[0]
                yield (items)#回傳資訊


class TVBSSpider(scrapy.Spider):
    kW = ''
    name = "news.tvbs.com.tw"#爬蟲名稱
    allowed_domains = ['news.tvbs.com.tw']#允許網域
    start_urls = [''] #起始網址
    ###拒絕網域
    rules = (
        Rule(LinkExtractor(deny=('news/searchresult/*')), callback = 'parse'))

    def parse(self, response):
        items = VscodeSshScrapyTestItem()#匯入items
        for n in response.css('body'):
            title = n.css('h1::text').get(default = '沒有抓到')#獲取標題
            #處理TVBS特殊標題格式
            items['title'] = title.replace('\u3000','')#去掉title(str)多餘的\u3000
            items['time'] = n.css('div.icon_time.time.leftBox2::text').get(default = '沒有抓到')#獲取文章日期、時間
            items['author'] = n.css('h4 > a::text').get(default = '沒有作者')#獲取作者
            content = n.css('div.h7.margin_b20 > p::text').getall() + n.css('div.h7.margin_b20::text').getall()#獲取文章內容
            items['content'] = self.ContentProcess(content)#文章內容處理
            items['source'] = 'TVBS'#文章來源
            items['keyword'] = self.kW
            items['url'] = self.start_urls[0]
            yield(items) #回傳資訊

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