from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
import logging
import json
from scrapy.conf import settings
from scrapy import http
from TW.items import TwItem
import scrapy


class TwComment(CrawlSpider):
    name = 'TW'

    # the name of the spider

    def start_requests(self):
        # 13个实时
        # urls = ['https://twitter.com', 'https://twitter.com/i/streams/category/686639666771046402',]
        # urls = ['https://twitter.com/i/streams/category/686639666779394057', 'https://twitter.com/i/streams/category/686639666779426835',]
        # urls = ['https://twitter.com/i/streams/category/686639666779394055', 'https://twitter.com/i/streams/category/686639666779426842',]
        # urls = ['https://twitter.com/i/streams/category/686639666779426845', 'https://twitter.com/i/streams/category/686639666779394072']
        # urls = ['https://twitter.com/i/streams/category/690675490684678145', 'https://twitter.com/i/streams/category/692079932940259328']
        # urls = ['https://twitter.com/i/streams/category/788602775839965184', 'https://twitter.com/i/streams/category/841388582518562816']
        # urls = ['https://twitter.com/i/streams/category/841390443338309632']

        # 88 个名人
        # urls = ['https://twitter.com/BarackObama', 'https://twitter.com/BillClinton']
        # urls = ['https://twitter.com/HillaryClinton','https://twitter.com/FLOTUS']
        # urls = ['https://twitter.com/mike_pence','https://twitter.com/KellyannePolls']
        # urls = ['https://twitter.com/MichelleObama','https://twitter.com/Pontifex']
        # urls = ['https://twitter.com/Queen_Europe','https://twitter.com/BillGates']
        # urls = ['https://twitter.com/David_Cameron','https://twitter.com/JeffBezos']
        # urls = ['https://twitter.com/narendramodi','https://twitter.com/Cristiano']
        # urls = ['https://twitter.com/KingJames','https://twitter.com/rogerfederer']
        # urls = ['https://twitter.com/neymarjr','https://twitter.com/RafaelNadal']
        # urls = ['https://twitter.com/StephenCurry30','https://twitter.com/DjokerNole']
        # urls = ['https://twitter.com/RondaRousey','https://twitter.com/serenawilliams']
        # urls = ['https://twitter.com/MariaSharapova','https://twitter.com/TheNotoriousMMA']
        # urls = ['https://twitter.com/kobebryant','https://twitter.com/KDTrey5']
        # urls = ['https://twitter.com/FloydMayweather','https://twitter.com/GalGadot']
        # urls = ['https://twitter.com/EmmaWatson','https://twitter.com/lizasoberano']
        # urls = ['https://twitter.com/NargisFakhri','https://twitter.com/russellcrowe']
        # urls = ['https://twitter.com/McConaughey','https://twitter.com/LeoDiCaprio']
        # urls = ['https://twitter.com/realdepp','https://twitter.com/RobertDowneyJr']
        # urls = ['https://twitter.com/TomCruise','https://twitter.com/justinbieber']
        # urls = ['https://twitter.com/khloekardashian','https://twitter.com/kourtneykardash']
        # urls = ['https://twitter.com/KendallJenner','https://twitter.com/nytimes']
        # urls = ['https://twitter.com/cnnbrk','https://twitter.com/BBCBreaking']
        # urls = ['https://twitter.com/Google','https://twitter.com/FoxNews']
        # urls = ['https://twitter.com/WhiteHouse','https://twitter.com/ABC']
        # urls = ['https://twitter.com/ImRaina','https://twitter.com/BreakingNews']
        # urls = ['https://twitter.com/gmail','https://twitter.com/Aly_Raisman']
        # urls = ['https://twitter.com/JohnWall','https://twitter.com/JHarden13']
        # urls = ['https://twitter.com/espn','https://twitter.com/CNN']
        # urls = ['https://twitter.com/NBA','https://twitter.com/GameOfThrones']
        # urls = ['https://twitter.com/SamuelLJackson','https://twitter.com/AntDavis23']
        # urls = ['https://twitter.com/jtimberlake','https://twitter.com/tomhanks']
        urls = ['https://twitter.com/mark_wahlberg','https://twitter.com/danielwuyanzu']
        # urls = ['https://twitter.com/TheLewisTan','https://twitter.com/adamcarolla']
        # urls = ['https://twitter.com/KyrieIrving','https://twitter.com/NiallOfficial']
        # urls = ['https://twitter.com/chelseahandler','https://twitter.com/twhiddleston']
        # urls = ['https://twitter.com/taylorswift13','https://twitter.com/chrishemsworth']
        # urls = ['https://twitter.com/MarvelStudios','https://twitter.com/Schwarzenegger']
        # urls = ['https://twitter.com/JimCameron','https://twitter.com/TheRock']
        # urls = ['https://twitter.com/OfficialKat', 'https://twitter.com/SophieT']
        # urls = ['https://twitter.com/Maisie_Williams','https://twitter.com/susmitchakrabo1']
        # urls = ['https://twitter.com/ladygaga','https://twitter.com/katyperry']
        # urls = ['https://twitter.com/KimKardashian','https://twitter.com/aplusk']
        # urls = ['https://twitter.com/rihanna','https://twitter.com/justdemi']
        # urls = ['https://twitter.com/rustyrockets','https://twitter.com/MileyCyrus']

        for url in urls:
            yield http.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        items = response.xpath(
            '//div[@class="js-tweet-text-container"]/p[@lang=\"en\"]/img[@class=\'Emoji Emoji--forText\']')
        for item in self.parse_tweet_item(items):
            yield item

        next_page_id = response.xpath(
            '//div[@class="js-tweet-text-container"]/p[@lang=\"en\"]/a[@class=\"twitter-atreply pretty-link js-nav\"]').xpath(
            'attribute::href').extract()

        for item in next_page_id:
            next_page = "https://twitter.com" + ''.join(item)
            yield response.follow(next_page, self.parse_page)

    def parse_tweet_item(self, items):
        for item in items:
            comment = TwItem()

            comment['content'] = item.xpath('ancestor::p/text()').extract()[0]
            comment['image'] = item.xpath('attribute::alt').extract()[0]
            comment['title'] = item.xpath('attribute::title').extract()[0]

            if comment['content'] == '':
                # If there is not text, we ignore the comment
                continue
            yield comment


