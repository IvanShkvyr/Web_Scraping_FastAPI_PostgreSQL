import json
import pathlib

from itemadapter import ItemAdapter
from scrapy import Spider, Item, Field
from scrapy.crawler import CrawlerProcess


BASE_DIR = pathlib.Path(__file__).parent.parent
file_link = BASE_DIR / 'spiders' / 'rivne_meteo.json'

class RivneMeteoItem(Item):
    air_temperature = Field()
    wind_speed = Field()
    the_amount_of_precipitation = Field()


class RivneMeteoPipeline(object):
    rivne_meteo = []
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        self.rivne_meteo.append({
            "air_temperature": adapter['air_temperature'],
            "wind_speed": adapter['wind_speed'],
            "the_amount_of_precipitation": adapter['the_amount_of_precipitation'],
        })

    def close_spider(self, spider):
        with open(file_link, 'w', encoding='utf-8') as fd:
            json.dump(self.rivne_meteo, fd, ensure_ascii=False)


class SpiderRivneMeteo(Spider):
    name = 'rivne'
    allowed_domains = ['unian.ua']
    start_urls = ['https://www.unian.ua/pogoda/85461-chernigiv']
    custom_settings = {
        'ITEM_PIPELINES': {
            RivneMeteoPipeline: 300,
        }
    }

    def parse(self, response):
        raw_air_temperature = response.xpath('/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[3]/div/text()').get().removesuffix('°')
        air_temperature = normalise_air_temperature(raw_air_temperature)
        wind_speed = float(response.xpath("/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[5]/b/text()").get().removesuffix(' м/с'))
        the_amount_of_precipitation = float(response.xpath("/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[4]/b/text()").get().removesuffix(' мм'))

        yield RivneMeteoItem(
                                air_temperature=air_temperature,
                                wind_speed=wind_speed,
                                the_amount_of_precipitation=the_amount_of_precipitation
                            )


def normalise_air_temperature(data):
    if data[0] == "-":
        data = float(data[1:])
        return - data
    return float(data[1:])



def get_meteo_rivne():
    process = CrawlerProcess()
    process.crawl(SpiderRivneMeteo)
    process.start()
    


if __name__ == '__main__':
    get_meteo_rivne()