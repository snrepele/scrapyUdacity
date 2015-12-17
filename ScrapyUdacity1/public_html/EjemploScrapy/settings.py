# -*- coding: utf-8 -*-

# Scrapy settings for EjemploScrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'EjemploScrapy'

SPIDER_MODULES = ['EjemploScrapy.spiders']
NEWSPIDER_MODULE = 'EjemploScrapy.spiders'
DOWNLOAD_DELAY = 1
ITEM_PIPELINES = {'EjemploScrapy.pipelines.SQL': 100}
#ITEM_PIPELINES = {'EjemploScrapy.pipelines.EjemploscrapyPipeline': 100}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'EjemploScrapy (+http://www.yourdomain.com)'
