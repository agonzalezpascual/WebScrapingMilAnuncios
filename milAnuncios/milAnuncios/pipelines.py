import sqlite3 as sq
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MilanunciosPipeline:
    def __init__(self):
        self.createconexion()
        self.createtable()

    # En este método vamos a crear la conexion
    def createconexion(self):
        self.conn = sq.connect("database.db")
        self.cur = self.conn.cursor()

    # Este método lo creamos para no tener la tabla llena,
    # en un programa real no lo necesitaríamos
    def createtable(self):
        self.cur.execute("""drop table if exists anuncios""")
        self.cur.execute("""create table anuncios(
                        title text,
                        text text,
                        tlf text
                        )""")

    def process_item(self, item, spider):
        self.storedb(item)
        return item

    # Con este método guardamos todo en la base de datos
    def storedb(self, item):
        # Vamos a mandar los datos de esta forma ya que así es más seguro
        self.cur.execute("""insert into anuncios values (?,?,?)""",
                         (item['title'][0],
                          item['text'][0],
                          item['tlf'],
                          ))
        self.conn.commit()
        self.conn.execute()
