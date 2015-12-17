from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from EjemploScrapy.items import EjemploscrapyItem
import scrapy

class MySpider(BaseSpider):
  preguntas = open("D:\Nube\Dropbox\TESIS DATA LEARNING\Scrapy\EjemploScrapy\EjemploScrapy\spiders\items.csv")
  #preguntas = open("C:\Users\Maria Leon\Dropbox\TESIS DATA LEARNING\Scrapy\EjemploScrapy\items.csv")
  name = "udacity2"
  allowed_domains = ["http://forums.udacity.com/tags/ud359/"]
  start_urls =[]
  for line in preguntas:
     urlCompuesta="http://forums.udacity.com"+line
     start_urls.append(urlCompuesta)
     urlForo = "http://forums.udacity.com"
  def parse(self, response):
     hxs = HtmlXPathSelector(response)
     print response
     titles = hxs.select("//div[@class='span9']")
     items = []
     for sel in titles:
        item = EjemploscrapyItem()
        item ["title"] = sel.select("//div[@class='headNormal']//h2//text()").extract()
        item ["text"] = sel.select("//div[@class='question-body']//p").extract()
        item ["respuest"]= sel.select("//div[@class='answer-body']").extract()
        item ["respuestDate"]= sel.select("//div[@class='item-right']//div[@class='post-update-info post-update-info-user']//strong//text()").extract()
        item ["date"]= sel.select("//table[@id='question-table']//div[@class='post-update-info post-update-info-user']//strong//text()").extract()
        item ["relatedTo"]= sel.select("//div[@id='item-right']//div[3]//a/text()").extract()
        item["seen"]=sel.select("//div[@class='span3']//div[@class='boxC']/p[3]/strong/text()").extract()
        item["user"] = sel.select("//div[@class='post-update-info post-update-info-user']//p[@class='ui']//a//@href").extract()
        item["link"] = urlCompuesta
        
        items.append(item)
     return items