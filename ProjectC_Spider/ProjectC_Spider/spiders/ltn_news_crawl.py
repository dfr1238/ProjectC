import scrapy
from bs4 import BeautifulSoup
class ltnNewsSpider(scrapy.Spider):
    name = "news.ltn.com.tw" #爬蟲名稱
    allowed_domains = ['news.ltn.com.tw/'] #允許網域
    start_urls = ['https://news.ltn.com.tw/news/politics/breakingnews/3177607'] #起始網址

    def parse(self, response):
        content = ''
        for news in response.xpath('/html/body/div[10]'):
                title = news.css('div.whitecon:nth-child(16) > h1:nth-child(1)::text').get(), #獲取標題(ltn的whitecon:nth-child(數目),數目要+1)
                time = news.css('.time::text').get(), #獲取文章時間
                author = news.xpath('/html/body/div[10]/section/div[5]/div[2]/p[1]/text()').re(r'〔\w+'), #獲取作者
                content_html = news.css('.text').get(), #獲取內文HTML
                content= ''.join('%s' %id for id in content_html) #將內文HTML轉換成String
                time=''.join('%s' %id for id in time) #將時間轉換成String
                soup = BeautifulSoup(content,"lxml") #創立BS4處理
                content=soup.get_text() #使用BS4將HTML轉至文字
                content=' '.join(content.split()) #去除額外的標籤與unicode的部分
                content = self.ContentProcess(content)
                time=' '.join(time.split()) #去除額外的標籤與unicode的部分
                source = '自由時報' #設定來源
                yield { #回傳資訊
                    'title' : title,
                    'time' : time,
                    'author' :author,
                    'content' :content,
                    'source':source,
                }
    def ContentProcess(self,content):#LTN內容處理
        content = str(content)
        wuwan_virus_ads='相關新聞請見︰「武漢肺炎專區」請點此，更多相關訊息，帶您第一手掌握。 '
        script_remove='var disable_onead_inread = (function(){ var rang0 = [ (new Date(\'2018-06-08T00:00:00+0800\')).getTime() ,(new Date(\'2018-06-30T23:59:59+0800\')).getTime() ,{ \'focus\': true } ]; if(check_onead_mobile_inread(rang0)){ return true; } return false; })(); function check_onead_mobile_inread(rang){ var now = (new Date()).getTime(); var show_door = false; if(now>=rang[0] && now<=rang[1]){ show_door = true; var cate = rang[2]; var show_category = cate[category] ? cate[category] : false; return (show_door && show_category) ? true : false; } return false; } if(disable_onead_inread){ googletag.cmd.push(function() { googletag.defineSlot(\'/21202031/01-news-foc-P-IR2\', [[1, 1], [728, 90], [640, 360]], \'ad-inread\').addService(googletag.pubads()); googletag.enableServices(); }); $(function(){ googletag.cmd.push(function() { googletag.display(\'ad-inread\'); }); }); }else{ $(function(){ var script = document.createElement(\'script\'); script.src = "assets/js/onead_ir_mir.js"; var el = document.getElementsByTagName("script")[0]; el.parentNode.insertBefore(script, el); }); } 不用抽 不用搶 現在用APP看新聞 保證天天中獎 點我下載APP 按我看活動辦法'
        content = content.replace(wuwan_virus_ads,'')
        content = content.replace(script_remove,'')
        return content