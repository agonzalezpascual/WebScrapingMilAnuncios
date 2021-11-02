import scrapy

#INFORMATIVA PARA VER EL CÓDIGO DIRIGIRSE A ANUNCIOSMULTI_SPIDER.PY

class QuoteSpider(scrapy.Spider):
    name = "title"
    start_urls = [
        "https://www.milanuncios.com/coches-de-segunda-mano/"
    ]

    def parse(self, response):
            title = response.css(".ma-AdCard-detail .ma-AdCard-titleLink ::text").extract()

            yield {"titletext": title}

#INFORMATIVA PARA VER EL CÓDIGO DIRIGIRSE A ANUNCIOSMULTI_SPIDER.PY