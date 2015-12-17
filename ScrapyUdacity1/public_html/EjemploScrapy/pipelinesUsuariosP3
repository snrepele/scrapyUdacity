# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#Este clase me sirve para guardar los datos dentro de una base de datos MYSQL

from MySQLdb import connect                                                        
from scrapy import log                                                             
from scrapy.exceptions import DropItem


class EjemploscrapyPipeline(object):
    def process_item(self, item, spider):
            return item

HOST = 'localhost'                                                                 
USER = 'root'                                                                    
PASSWD = ''                                                           
DB = 'udacity'                                                                      


class SQL(object):                                                                 
    def open_spider(self, spider):                                                 
        self.dbcon = connect(host=HOST,                                            
                             user=USER,                                            
                             passwd=PASSWD,                                        
                             db=DB)                                                
        self.cursor = self.dbcon.cursor()                                          

    def process_item(self, item, spider):
        self.cursor.execute("select * from usuario where idUser = %s", (item["user"]))
        result=self.cursor.fetchone()
        if not result:
           self.cursor.execute("INSERT INTO usuario(idUser,name,bio,memberSince,age,lastSeen,karma,location) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (item['user'],item["name"],item["bio"],item["memberSince"],item["age"], item["lastSeen"],item["karma"],item["location"]))
        else:
           print "***************Usuario ya ingresado********************"
        return item                                                                

    def close_spider(self, spider):                                                
        self.dbcon.commit()
