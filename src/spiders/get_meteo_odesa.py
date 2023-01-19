import json
import pathlib

from itemadapter import ItemAdapter
from scrapy import Spider, Item, Field
from scrapy.crawler import CrawlerProcess


BASE_DIR = pathlib.Path(__file__).parent.parent
file_link = BASE_DIR / 'spiders' / 'odesa_meteo.json'

class OdesaMeteoItem(Item):
    air_temperature = Field()
    wind_speed = Field()
    the_amount_of_precipitation = Field()


class OdesaMeteoPipeline(object):
    odesa_meteo = []
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        self.odesa_meteo.append({
            "air_temperature": adapter['air_temperature'],
            "wind_speed": adapter['wind_speed'],
            "the_amount_of_precipitation": adapter['the_amount_of_precipitation'],
        })


    def close_spider(self, spider):

        with open(file_link, 'w', encoding='utf-8') as fd:
            json.dump(self.odesa_meteo, fd, ensure_ascii=False)


class SpiderOdesaMeteo(Spider):
    name = 'odesa'
    allowed_domains = ['gismeteo.ua']
    start_urls = ['https://www.gismeteo.ua/ua/weather-odessa-4982/now/']
    custom_settings = {
        'ITEM_PIPELINES': {
            OdesaMeteoPipeline: 300,
        }
    }


    def parse(self, response):
        content = response.xpath("/html//div[@class='now']")
        air_temperature = float(content.xpath("div/span[@class='unit unit_temperature_c']/text()").get())
        sign_air_temperature = content.xpath("div/span/span[@class='sign']/text()").get()
        if sign_air_temperature == '-':
            air_temperature = - float(air_temperature)
        wind_speed = float(content.xpath("/html/body/section/div[1]/section[3]/div/div[6]/div/div[1]/div[2]/div[1]/text()").get())
        the_amount_of_precipitation = float(content.xpath("/html/body/section/div[1]/section[3]/div/div[6]/div/div[2]/div[2]/div[1]/text()").get())

        yield OdesaMeteoItem(
                                air_temperature=air_temperature,
                                wind_speed=wind_speed,
                                the_amount_of_precipitation=the_amount_of_precipitation
                            )

def get_meteo_odesa():
    process = CrawlerProcess()
    process.crawl(SpiderOdesaMeteo)
    process.start()
    


if __name__ == '__main__':
    get_meteo_odesa()
