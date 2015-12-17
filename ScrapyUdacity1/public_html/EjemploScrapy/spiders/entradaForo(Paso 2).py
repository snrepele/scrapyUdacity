from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from EjemploScrapy.items import EjemploscrapyItem
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.http.request import Request
import re

class MySpider(BaseSpider):
  preguntas = open("D:\Nube\Dropbox\TESIS DATA LEARNING\Scrapy\EjemploScrapy\EjemploScrapy\spiders\items.csv")
  #preguntas = open("C:\Users\Maria Leon\Dropbox\TESIS DATA LEARNING\Scrapy\EjemploScrapy\items.csv")
  name = "udacity2"
  start_urls =[]
  TAG_RE = re.compile(r'<[^>]+>')
  handle_httpstatus_list = [404]
  #start_urls.append("http://forums.udacity.com/questions/100115939/problem-set-2-problem-13-confused-on-this-question")
  for line in preguntas:
   urlCompuesta="http://forums.udacity.com"+line
   start_urls.append(urlCompuesta)
  urlForo = "http://forums.udacity.com"
  def parse(self, response):
     if response.status == 404:
         print "ERROR 404 %s", response.url
         self.start_urls.append(response.url)
         yield Request(response.url,self.parse)
     hxs = HtmlXPathSelector(response)
     titles = hxs.select("//div[@class='span9']")
     items = []
     
     if(titles):
      for sel in titles:
        item = EjemploscrapyItem()
        title = sel.select("//div[@class='headNormal']//h2//text()").extract()
        var = response.url
        idPost1 = var.split('/')
        item["idPost"]=idPost1[4]
 
        item["title"] = title[0]
        item ["text"] = sel.select("//div[@class='question-body']//*").extract()
        item ["text"] = ' '.join(item["text"])
        item["text"] = self.TAG_RE.sub('', item["text"])
        item["title"]=item["title"].encode('ascii',errors='ignore')
        
        #NUMERO DE VOTOS DEL POST SOLO UN VALOR
        votes=sel.select("//table[@id='question-table']//h3//text()").extract()
        item["votes"] = votes
        
        item["votes"] =item["votes"][0].strip()
        item["votes"]=item["votes"].encode('ascii',errors='ignore')
        #NUMERO DE RESPUESTAS  SOLO UN VALOR
        numberRespuests=sel.select("//div[@class='headQuestions']//h2//text()").extract()
        if numberRespuests:
            item["numberRespuests"] = numberRespuests[1].replace('\n','')
            item["numberRespuests"] =item["numberRespuests"].strip()
            if "One" in item["numberRespuests"]:
               item["numberRespuests"] ="1"
            
            item["numberRespuests"] = re.sub("\D", "", item["numberRespuests"])
            item["numberRespuests"] = item["numberRespuests"].encode('ascii',errors='ignore')
        else:
            item["numberRespuests"] = "0"

        
        
        #*********TEXTO DE CADA RESPUESTA ARREGLO
        respuestas= sel.select("//div[@class='answer-body']").extract()
        respuestaAux =[]
        for respuesta in respuestas:
                   respuesta =respuesta.replace('<div class=\"answer-body\">\n ','')
                   #respuesta = respuesta.replace('</div>', '')
                   
                   respuesta = respuesta.encode('ascii',errors='ignore')
                   respuesta= self.TAG_RE.sub('', respuesta) #LIMPIAR DE HTML
                   respuesta = respuesta.strip()
                   respuestaAux.append(respuesta)
                   
        item["respuest"]= respuestaAux
           
        #*****************TEXTO DE CADA COMENTARIO
        comments =sel.select("//div[@class='comment-text']").extract()
        commentsAux =[]
        for com in comments:
             #com = com.replace("class=\"comment-text\">","")
             #com = com.replace("</div>","")
             #com = com.replace("<div","")
             com = com.encode('ascii',errors='ignore')#CODIFICANDOOOOOOOOOOOOO
             com = com.strip()
             com= self.TAG_RE.sub('', com)
             commentsAux.append(com)
        #**********************************************

        #**********IDENTIFICADOR DE CADA COMENTARIO
        idComment = sel.select("//div[@class='comment']/@id").extract()
        auxiliarIdComment =[]
        for idCom in idComment:
               aux= hxs.select("//div[@id='"+idCom+"']/../@id").extract()
               if re.sub("\D", "", aux[0])==item["idPost"]:
                 aux[0] = aux[0].replace("comments-container-","idPost ")
               else:
                 aux[0] = aux[0].replace("comments-container-","idRespuest ")
               idCom = idCom.replace("comment-","")
               auxiliarIdComment.append(idCom+" "+aux[0])
        #**********************************************   
        #***********ID DE CADA USUARIO DE COMENTARIOS
        idUserComment = sel.select("//div[@class='comment']//a[@class='comment-user userinfo']//@href").extract()
        #**********************************************
        #***********FECHAS DE COMENTARIOS**********
        dateComment = sel.select("//div[@class='comment']//div[@class='comment-info']//span[@class='comment-age']//text()").extract()
        datComAux= []
        for dtCo in dateComment:
             dtCo= dtCo.replace("(","")
             dtCo= dtCo.replace(")","")
             datComAux.append(dtCo)
        #******************************************+
         #ASIGACION A ITEMS  PARA EXPORTACION DE DATOS COMENTARIOS
        item["comments"] = commentsAux
        item["idComment"] =auxiliarIdComment
        item["dateComment"]= datComAux
        item["idUserComment"]= idUserComment
         
        item ["respuestDate"]= sel.select("//div[@class='item-right']//div[@class='post-update-info post-update-info-user']//strong//text()").extract()
        idRespuesta = sel.select("//div[@id='askform']/a[@name]").extract()
        idRes= []
        voteRespuest = []
        #ID DE RESUPESTAS
        for idR in idRespuesta:
                  idR =re.sub("\D", "", idR)
                  idRes.append(idR)
                  #VOTOS DE RESPUESTAS ARREGLO
                  vR =sel.select("//div[@id='answer-container-"+idR+"']//h3//text()").extract()
                  voteRespuest.append(vR[0])
        item["idRespuest"]=idRes
        item["voteRespuest"]=voteRespuest
        date= sel.select("//table[@id='question-table']//div[@class='post-update-info post-update-info-user']//strong//text()").extract()
        item["date"] =date[0]

        relatedTo= sel.select("//div[@id='item-right']//div[3]//a/text()").extract()
        if relatedTo:
           item ["relatedTo"] =relatedTo[0]
        else:
           item["relatedTo"] = "null"
        seen =sel.select("//div[@class='span3']//div[@class='boxC']/p[3]/strong/text()").extract()
        item["seen"]= seen[0]

        item["user"] = sel.select("//div[@class='post-update-info post-update-info-user']//p[@class='ui']//a//@href").extract()
        auxUser=[]
        for user in item["user"]:
            auxUser.append(user.encode('ascii',errors='ignore'))
        item["user"]= auxUser
        item["relatedTo"] = item["relatedTo"].encode('ascii',errors='ignore')
        item["text"]=item["text"].encode('ascii',errors='ignore')
        items.append(item)

        #SE DEBE ENVIAR LOS PARAMETROS A GUARDAR CON YIELD NO CON RETURN PUES UTILIZO FUNCIONES EN CICLO RECURSIVAS
        # for item in items:
        
         #LAS SIGUIENTES LINEAS DE CODIGO CONSIDERAN SI EXISTIESE UNA SIGUIENTE PAGINA DE COMENTARIOS DENTRO DE LA ENTRADA DE FORO
        yield item
        next_page= sel.select("//span[@class='next']//@href").extract()
        if  next_page:    
           print "*******************************NEXT PAGE*********************************"
           direccion= "http://forums.udacity.com" + next_page[0]
           print direccion
           if direccion not in self.start_urls:
              print "***********AnADIRE LA DIRECCION**************************************"
              #self.start_urls.append(direccion)
              yield Request(direccion,self.parse)
        