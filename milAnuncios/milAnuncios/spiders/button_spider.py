import scrapy
import ast

#INFORMATIVA PARA VER EL CÓDIGO DIRIGIRSE A ANUNCIOSMULTI_SPIDER.PY

class QuoteSpider(scrapy.Spider):
    name = "button"
    start_urls = [
        "https://www.milanuncios.com/api/freespee/contact.php?adId=426044407"
    ]

    def parse(self, response):
        json = ast.literal_eval(response.body.decode('UTF-8'))
        telf = json["phone"]
        yield {"a":telf}

#INFORMATIVA PARA VER EL CÓDIGO DIRIGIRSE A ANUNCIOSMULTI_SPIDER.PY