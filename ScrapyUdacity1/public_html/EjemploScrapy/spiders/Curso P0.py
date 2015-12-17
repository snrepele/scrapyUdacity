from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from EjemploScrapy.items import EjemploscrapyItem
import scrapy
import re
from scrapy.http.request import Request
#Esta clase tiene como objetivo extraer los principales links de cada una de las paginas de entrada de foro . 



class MySpider(BaseSpider):
  
  name = "udacity0"
  start_urls =[]
  urlCompuesta="https://www.udacity.com/courses#!/all"
  #urlCompuesta= "https://www.udacity.com/course/nd001"
  start_urls.append(urlCompuesta)
  urlForo = "http://forums.udacity.com"
  i=0
  TAG_RE = re.compile(r'<[^>]+>')
  def parse(self, response):
      hxs = HtmlXPathSelector(response)
      print response
      items = []
      i=0
      item = EjemploscrapyItem()
      for sel in response.xpath("//div[@class='row']"):
          item = EjemploscrapyItem()
          #item ["title"] = sel.select("a/text()").extract()
          link = sel.select("//h2/a/@href").extract()
          #self.start_urls.append(link)
      for lk in link:
          request = scrapy.Request("http://www.udacity.com"+link[i],callback=self.parse2)
          
          #callback=self.parse2
          items.append(request)
          i=i+1
      return items
  def parse2(self,response):  
      hxs = HtmlXPathSelector(response)
      print response
      item = EjemploscrapyItem()
      title = hxs.select("//h1/text()").extract()
      title1 = title[0].replace("\t","")
      item ['title']= title1.replace("\n","")
      item ["idCourse"] = str(response)
      item["idCourse"] =item["idCourse"].replace("HtmlResponse","")
      item["idCourse"] =item["idCourse"].replace("200", "")
      item["idCourse"] =item["idCourse"].split("/")
      item["idCourse"] =item["idCourse"][4]
      item["idCourse"] =item["idCourse"].replace('>"','')
      item["idCourse"] =item["idCourse"].replace('"','')
      item ["summary"]= hxs.select("//div[@class='row row-gap-large']//div[@class='pretty-format']/*").extract()
      
      if item["title"].find("Nanodegree") > 0:
         print ":::::::::::::HOLA NO HAY SUMMAYRYYYYYYYYYYYYYYYYYYYYY::::::::::::::::"
         item ["summary"]= hxs.select("//div[@class='row']//div[@class='col-xs-12 ']//div[@class='pretty-format']/*").extract()
      item["summary"] = ' '.join(item["summary"])
      
      
      item["summary"]=item["summary"].encode('ascii',errors='ignore')
      item["title"]=item["title"].encode('ascii',errors='ignore')
      item["idCourse"]=item["idCourse"].encode('ascii',errors='ignore')
      item["summary"]= self.TAG_RE.sub('', item["summary"])
      return item