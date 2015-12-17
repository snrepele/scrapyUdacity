from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from EjemploScrapy.items import EjemploscrapyItem
import scrapy
import json
import re
class MySpider(BaseSpider):
  with open('D:\Nube\Dropbox\TESIS DATA LEARNING\Scrapy\EjemploScrapy\EjemploScrapy\spiders\cursoPsicologiaUltimo.json') as foros:
     data=json.load(foros)
  #with open('C:\Users\Maria Leon\Dropbox\TESIS DATA LEARNING\Scrapy\EjemploScrapy\loros.json') as foros:
     #data=json.load(foros)
  
  name = "udacity3"
  start_urls =[]
  usuarios =[]
  var=0
  TAG_RE = re.compile(r'<[^>]+>')
  handle_httpstatus_list = [404]
  #CARGAR TODOS LOS USUARIOS DEL ARCHIVO DE FOROS :CARGA USUARIOS QUE ESCRIBEN RESPUESTAS Y COMENTARIOS EN EL SEGUNDO FOR
  for line in data:
    usuarios=data[var]["user"]
    usuariosComentarios = data[var]["idUserComment"]
    for i in range(len(usuarios)):
       user=data[var]["user"][i]
       urlCompuesta="http://forums.udacity.com"+user
       if urlCompuesta not in start_urls:
           start_urls.append(urlCompuesta)
    for j in range(len(usuariosComentarios)):
       user1= data[var]["idUserComment"][j]
       urlCompuesta="http://forums.udacity.com"+user1
       if urlCompuesta not in start_urls:
           start_urls.append(urlCompuesta)
    var=var+1
    
  def parse(self, response):
     if response.status == 404:
         print "ERROR 404 %s", response.url
         self.start_urls.append(response.url)
         yield Request(response.url,self.parse)
     hxs = HtmlXPathSelector(response)
     print response
     titles = hxs.select("//div[@id='mainbar-full']")
     items = []
     for sel in titles:
        item = EjemploscrapyItem()
        var = response.url
        idUser = var.split('/')
        item["user"]=idUser[3]+"/"+idUser[4]+ "/"+idUser[5]
        items.append(item)
        item ["name"] = sel.select("//div[@class='headUser']//text()").extract()
        item["name"] = str(item["name"])
        item["name"] = item["name"].replace("u'\\n", "").replace("\\n","")
        item["name"] = item["name"].replace("[","")
        item["name"] = item["name"].replace("]","")
        item["name"] = item["name"].replace("'","")
        item["name"] = item["name"].strip()
        item["name"] = item["name"].encode('ascii',errors='ignore')
        memberSince= sel.select("//table[@class='user-details']//tr[2]//td[2]//strong//text()").extract()
        item ["memberSince"] = memberSince[0]
        
        lastSeen= sel.select("//table[@class='user-details']//tr[3]//td[2]//strong//text()").extract()
        item ["lastSeen"]= lastSeen[0]
        #PROBLEMA PUES LA TABLA CAMBIA CUANDO NO HAY DATOS DE EDAD O DE LOCALIZACION POR LO QUE SE DEBE CONSULTAR QUE DICE EL CAMPO FRENTE A EL
        
        
        existenDatos=sel.select("//table[@class='user-details']//tr[4]//td[1]//text()").extract()
       
        if existenDatos:
            if "website" in existenDatos[0]: #SI TIENE WEB SITE SE CORRERA UNA POSICION LOCATION Y AGE
               print "SI TIENE WEBSITE"
               posicionCuatroTabla=sel.select("//table[@class='user-details']//tr[5]//td[1]//text()").extract()
               if posicionCuatroTabla:#SI EXISTE ALGO EN LA POSICION DESPUES DE WEBSITE
                    if "location" in posicionCuatroTabla[0]:# SI ESTE VALOR ES LOCATION BUSCAR LOCATION Y AGE
                       location = sel.select("//table[@class='user-details']//tr[5]//td[2]//text()").extract()
                       age= sel.select("//table[@class='user-details']//tr[6]//td[2]//text()").extract()
                    if "age" in posicionCuatroTabla[0]:#SI ESTE VALOR ES AGE SOLO SE BUSCA AGE Y LOCATION SE UBICA EN NADA
                       age= sel.select("//table[@class='user-details']//tr[5]//td[2]//text()").extract()
                       location = ""
               else:
                    age=""
                    location =""
                    
            if "location" in existenDatos[0]:#EN CASO DE DE  NO SEA WEBSITE EL CAMPO  NUMERO 4
                location = sel.select("//table[@class='user-details']//tr[4]//td[2]//text()").extract()
                age= sel.select("//table[@class='user-details']//tr[5]//td[2]//text()").extract()
            if "age" in existenDatos[0]:
                age= sel.select("//table[@class='user-details']//tr[4]//td[2]//text()").extract()
                location= ""
        else:
            location = ""
            age = ""
        if location:
           item ["location"]= location[0].encode('ascii',errors='ignore')
        else: 
           item["location"]= "null"
        
        
        if age:item["age"]= re.sub("\D", "", age[0])
        else: item["age"] = "0"
        karma = sel.select("//div[@id='user-reputation']//text()").extract()
        item["karma"] = karma[0]

        bio =  sel.select("//div[@class='user-about']//text()").extract()
        bio = ' '.join(bio)
        bio = self.TAG_RE.sub('', bio)
        bio = bio.strip()
        bio = bio.replace('\n','')
        if bio:item["bio"] = bio
        else: item["bio"] = "null"
        item["bio"] = item["bio"].encode('ascii',errors='ignore')
        items.append(item)
     yield item