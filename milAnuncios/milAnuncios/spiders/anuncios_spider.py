import scrapy
import ast

from ..items import MilanunciosItem

#INFORMATIVA PARA VER EL CÓDIGO DIRIGIRSE A ANUNCIOSMULTI_SPIDER.PY

class QuoteSpider(scrapy.Spider):
    name = "anuncios"
    start_urls = [
        "https://www.milanuncios.com/coches-de-segunda-mano/"
    ]

    def parse(self, response):

        cartas = response.css(".ma-AdCard")
        #text = response.css(".ma-AdCardDescription-text::text").extract()
        #title = response.css(".ma-AdCard-detail .ma-AdCard-titleLink ::text").extract()
        for c in cartas:
            next_page = c.css(" .ma-AdCard-adId::text").extract()
            text = c.css(".ma-AdCardDescription-text::text").extract()
            title = c.css(".ma-AdCard-detail .ma-AdCard-titleLink ::text").extract()
            numero = 'https://www.milanuncios.com/api/freespee/contact.php?adId=' + str(next_page[1])
            tlf = scrapy.Request(numero, callback=self.parse_num)
            tlf.meta["text"]= text
            tlf.meta["title"] = title
            yield tlf

# INFORMATIVA PARA VER EL CÓDIGO DIRIGIRSE A ANUNCIOSMULTI_SPIDER.PY

    def parse_num(self, response):
        items = MilanunciosItem()
        text = response.meta["text"]
        title = response.meta["title"]
        json = ast.literal_eval(response.body.decode('UTF-8'))
        telf = json["phone"]
        items["title"]=title
        items["text"]=text
        items["tlf"]=telf


        yield items


#INFORMATIVA PARA VER EL CÓDIGO DIRIGIRSE A ANUNCIOSMULTI_SPIDER.PY