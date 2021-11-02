import scrapy
import ast

from ..items import MilanunciosItem

# Declaro las variables iniciales de la spider
class QuoteSpider(scrapy.Spider):
    #nombre de la spider
    name = "anunciosm" #Para ejecutar usamos scrapy crawl anunciosm
    #Esta variable me servirá después para cambiar de página
    pag = 1
    start_urls = [
        "https://www.milanuncios.com/coches-de-segunda-mano/"
    ]

    def parse(self, response):
        #Creo esta variable para iterar sobre cada uno de los anuncios,
        # y así enviarlo en un formato más legible a la base de datos
        cartas = response.css(".ma-AdCard")
        for c in cartas:
            #Scrapeo la id del anuncio para poder acceder al teléfono
            next_page = c.css(" .ma-AdCard-adId::text").extract()
            #Scrapeo el texto del anuncio
            text = c.css(".ma-AdCardDescription-text::text").extract()
            #Scrapeo el título del anuncio
            title = c.css(".ma-AdCard-detail .ma-AdCard-titleLink ::text").extract()
            #Con esta variable entro a la página que contiene el anuncio
            numero = 'https://www.milanuncios.com/api/freespee/contact.php?adId=' + str(next_page[1])
            #Mediante el método Request accedo a la página del teléfono
            tlf = scrapy.Request(numero, callback=self.parse_num)
            #Mediante el método meta mando variables a la clase parse_num,
            #en la ocurre el scrapeo del teléfono
            tlf.meta["text"]= text
            tlf.meta["title"] = title
            yield tlf

    #Función encargada de parsear el número de teléfono, devolver los items y moverse a la siguiente página
    def parse_num(self, response):
        #Instancio un objeto de tipo Item para mandarlo a la pipeline
        items = MilanunciosItem()
        #Recupero las variables antes mencionadas
        text = response.meta["text"]
        title = response.meta["title"]
        #Así extraigo el archivo Json en el que se encuentra el teléfono
        json = ast.literal_eval(response.body.decode('UTF-8'))
        telf = json["phone"]
        #Asigno los resultados al objeto Item para poder pasárselo a pipelines
        items["title"]=title
        items["text"]=text
        items["tlf"]=telf
        #Creo la url necesaria para poder moverme a la siguiente página
        pagina = "https://www.milanuncios.com/coches-de-segunda-mano/?nextToken=eyJkaXIiOiJmIiwiaWQiOiI0MjY1MTgxMDMiLCJkYXRlIjoxNjM0NzY3OTg3MDAwLCJwcmljZSI6MzE0OTksImN1cnJlbnRQYWdlIjoxfQ%3D%3D&pagina=" + str(QuoteSpider.pag)

        #Paso los objetos a pipelines
        yield items
        #Hago una comprobación de que no hayamos pasado las 200 páginas
        if QuoteSpider.pag<=199:
            QuoteSpider.pag +=1
            #Por último vuelvo a llamar al método parse con la url de la siguiente página
            yield response.follow(pagina, callback=self.parse)