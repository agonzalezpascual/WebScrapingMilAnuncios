import scrapy
import ast

#INFORMATIVA PARA VER EL CÓDIGO DIRIGIRSE A ANUNCIOSMULTI_SPIDER.PY

class NumeroSpider(scrapy.Spider):
    name = "numero"
    start_urls = [
        "https://www.milanuncios.com/coches-de-segunda-mano/"
    ]


    def parse_num(self, response):
        json = ast.literal_eval(response.body.decode('UTF-8'))
        telf = json["phone"]
        yield {"a":telf}

    def parse(self, response):
        next_page = response.css(" .ma-AdCard-adId::text").extract()
        next_page = [x for x in next_page if x != 'r']

        for n in next_page:
            url = 'https://www.milanuncios.com/api/freespee/contact.php?adId=' + n
            yield response.follow(url, callback=self.parse_num)

#INFORMATIVA PARA VER EL CÓDIGO DIRIGIRSE A ANUNCIOSMULTI_SPIDER.PY