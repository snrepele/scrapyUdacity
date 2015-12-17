# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#Este archivo pipelines sirve en la parte de extraccion de foros donde se duplicaban los datos ..es una version previa pues no guarda en base de datos solo sirve para guardar en json
from scrapy.exceptions import DropItem
import json
class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['respuest'][0] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            for it in item["respuest"]:
              self.ids_seen.add(it)
              return item