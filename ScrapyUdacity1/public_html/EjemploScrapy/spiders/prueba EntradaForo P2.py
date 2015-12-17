from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from EjemploScrapy.items import EjemploscrapyItem
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http.request import Request
import re

class MySpider(BaseSpider):
  name = "udacityP"
  start_urls =[]
  items = []
  urlCompuesta= "http://forums.udacity.com/questions/100073352/lesson-5-marriage-age?sort=votes&page=1#ps001"
  start_urls.append(urlCompuesta)
  def parse(self, response):
      hxs = HtmlXPathSelector(response)  
      titles = hxs.select("//div[@class='span9']")
      items= []
      urlCompuesta= "http://forums.udacity.com/questions/100073352/lesson-5-marriage-age?sort=votes&page=1#ps001"
      #SI EXISTE ES DE FOROS
      if(titles):
       for sel in titles:      
         item = EjemploscrapyItem()
         title = sel.select("//div[@class='headNormal']//h2//text()").extract()
         item["title"] = title[0]

         item ["text"] = sel.select("//div[@class='question-body']//*").extract()
         item ["text"] = ' '.join(item["text"])

         respuestas= sel.select("//div[@class='answer-body']").extract()
         respuestaAux =[]
         for respuesta in respuestas:
                   respuesta =respuesta.replace('<div class=\"answer-body\">\n ','')
                   respuesta = respuesta.replace('</div>', '')
                   respuesta = respuesta.strip()
                   respuestaAux.append(respuesta)
         item["respuest"]= respuestaAux
        
         
         comments =sel.select("//div[@class='comment-text']").extract()
         commentsAux =[]
         for com in comments:
              com = com.replace("class=\"comment-text\">","")
              com = com.replace("</div>","")
              com = com.replace("<div","")
              commentsAux.append(com)
         
         idComment = sel.select("//div[@class='comment']/@id").extract()
         auxiliarIdComment =[]
         for idCom in idComment:
                aux= hxs.select("//div[@id='"+idCom+"']/../@id").extract()
                aux[0] = aux[0].replace("comments-container-","idRespuest:")
                idCom = idCom.replace("comment-","")
                auxiliarIdComment.append(idCom+" "+aux[0])
                
         idUserComment = sel.select("//div[@class='comment']//a[@class='comment-user userinfo']//@href").extract()
         
         dateComment = sel.select("//div[@class='comment']//div[@class='comment-info']//span[@class='comment-age']//text()").extract()
         datComAux= []
         for dtCo in dateComment:
              dtCo= dtCo.replace("(","")
              dtCo= dtCo.replace(")","")
              datComAux.append(dtCo)
         #ASIGACION A ITEMS  PARA EXPORTACION DE DATOS
         item["comments"] = commentsAux
         item["idComment"] =auxiliarIdComment
         item["dateComent"]= datComAux
         item["idUserComment"]= idUserComment
         
         item ["respuestDate"]= sel.select("//div[@class='item-right']//div[@class='post-update-info post-update-info-user']//strong//text()").extract()

         idRespuesta = sel.select("//div[@id='askform']/a[@name]").extract()
         idRes= []
         for idR in idRespuesta:
                   idR =re.sub("\D", "", idR)
                   idRes.append(idR)
         item["idRespuest"]=idRes


         date= sel.select("//table[@id='question-table']//div[@class='post-update-info post-update-info-user']//strong//text()").extract()
         item["date"] =date[0]

         relatedTo= sel.select("//div[@id='item-right']//div[3]//a/text()").extract()
         item ["relatedTo"] =relatedTo[0]
         
         seen =sel.select("//div[@class='span3']//div[@class='boxC']/p[3]/strong/text()").extract()
         item["seen"]= seen[0]
         
         item["user"] = sel.select("//div[@class='post-update-info post-update-info-user']//p[@class='ui']//a//@href").extract()
 
         idPost1 = urlCompuesta.split('/')
         item["idPost"]=idPost1[4]
         items.append(item)

        #SE DEBE ENVIAR LOS PARAMETROS A GUARDAR CON YIELD NO CON RETURN PUES UTILIZO FUNCIONES EN CICLO RECURSIVAS
        # for item in items:
         yield item
                #LAS SIGUIENTES LINEAS DE CODIGO CONSIDERAN SI EXISTIESE UNA SIGUIENTE PAGINA DE COMENTARIOS DENTRO DE LA ENTRADA DE FORO
         next_page= sel.select("//span[@class='next']//@href").extract()
         if  next_page:
            print "*******************************NEXT PAGE*********************************"
            direccion= "http://forums.udacity.com" + next_page[0]
            yield Request(direccion,self.parse)