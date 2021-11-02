import scrapy

#INFORMATIVA PARA VER EL CÓDIGO DIRIGIRSE A ANUNCIOSMULTI_SPIDER.PY

class QuoteSpider(scrapy.Spider):
    name = "text"
    start_urls = [
        "https://www.milanuncios.com/coches-de-segunda-mano/"
    ]

    def parse(self, response):

        text = response.css(".ma-AdCardDescription-text::text").extract()

        yield {"text": text}

#INFORMATIVA PARA VER EL CÓDIGO DIRIGIRSE A ANUNCIOSMULTI_SPIDER.PY