from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from EjemploScrapy.items import EjemploscrapyItem
import scrapy

#Esta clase tiene como objetivo extraer los principales links de cada una de las paginas de entrada de foro . Recorre la Paginacion de los foros #ESta cnfigurada para el foro de Psicologia



class MySpider(BaseSpider):
  
  name = "udacity1"
  start_urls =[]
  start_urls.append("http://forums.udacity.com/tags/ps001/#ps001")
  #LISTA DE PAGINACION DEL FORO DEL CURSO PS001
  for i in range(38):
      urlCompuesta="http://forums.udacity.com/tags/ps001/?sort=active&page="+str(i)+"&pagesize=50#ps001"
      start_urls.append(urlCompuesta)
      urlForo = "http://forums.udacity.com"
  def parse(self, response):
      hxs = HtmlXPathSelector(response)
      print response
      #titles = hxs.select("//div[@class='span9']")
      items = []
      for sel in response.xpath('//h2'):
          item = EjemploscrapyItem()
          item ["link"] = sel.select("a/@href").extract()
          if item["link"]:
             items.append(item)
      return items