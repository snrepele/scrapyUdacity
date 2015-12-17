from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from EjemploScrapy.items import EjemploscrapyItem
import scrapy
import json
class MySpider(BaseSpider):
  name = "usuarios"
  start_urls =[]
  urlCompuesta=  "http://forums.udacity.com/users/122612557/sanne-4#ps001"
  start_urls.append(urlCompuesta)
  
  def parse(self, response):
     hxs = HtmlXPathSelector(response)
     print response
     titles = hxs.select("//div[@id='mainbar-full']")
     items = []
     for sel in titles:
        item = EjemploscrapyItem()
        item ["name"] = sel.select("//div[@class='headUser']//text()").extract()
        item["name"] = str(item["name"])
        item["name"] = item["name"].replace("u'\\n", "").replace("\\n","")
        item ["memberSince"] = sel.select("//table[@class='user-details']//tr[2]//td[2]//strong//text()").extract()
        item ["lastSeen"]= sel.select("//table[@class='user-details']//tr[3]//td[2]//strong//text()").extract()
        item ["location"]= sel.select("//table[@class='user-details']//tr[5]//td[2]//text()").extract()
        item["age"]=sel.select("//table[@class='user-details']//tr[6]//td[2]//text()").extract()
        item["karma"] = sel.select("//div[@id='user-reputation']//text()").extract()
        item["bio"] = sel.select("//div[@class='user-about']//p//text()").extract()
        items.append(item)
     return items