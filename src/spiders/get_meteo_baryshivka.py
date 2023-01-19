import json
import pathlib

from itemadapter import ItemAdapter
from scrapy import Spider, Item, Field
from scrapy.crawler import CrawlerProcess

BASE_DIR = pathlib.Path(__file__).parent.parent
file_link = BASE_DIR / 'spiders' / 'baryshivka_meteo.json'


class BaryshivkaMeteoItem(Item):
    air_temperature = Field()
    wind_speed = Field()
    the_amount_of_precipitation = Field()
    

class BaryshivkaMeteoPipeline(object):
    baryshivka_meteo = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        self.baryshivka_meteo.append({
            "air_temperature": adapter['air_temperature'],
            "wind_speed": adapter['wind_speed'],
            "the_amount_of_precipitation": adapter['the_amount_of_precipitation'],
        })

    def close_spider(self, spider):

        avr_baryshivka_meteo = avr_meteo(self.baryshivka_meteo)
        
        with open(file_link, 'w', encoding='utf-8') as fd:
            json.dump(avr_baryshivka_meteo, fd, ensure_ascii=False)


class SpiderBaryshivkaMeteo(Spider):
    name = 'baryshivka'
    allowed_domains = ['cgo-sreznevskyi.kyiv.ua']
    start_urls = ['http://www.cgo-sreznevskyi.kyiv.ua/uk/pro-tsho/merezha/ohms-baryshivka']
    custom_settings = {
        'ITEM_PIPELINES': {
            BaryshivkaMeteoPipeline: 300,
        }
    }


    def parse(self, response):

        for row in response.xpath('//*[@id="sp-component"]/div/article/div[2]/table/tbody/tr'):
            if row.xpath('td[3]//text()').extract_first():
                           
                raw_air_temperature = row.xpath('td[3]//text()').extract_first()
                air_temperature = normalise_data(raw_air_temperature)
                raw_wind_speed = row.xpath('td[5]//text()').extract_first()
                wind_speed = normalise_data(raw_wind_speed)
                raw_the_amount_of_precipitation = row.xpath('td[7]//text()').extract_first()
                the_amount_of_precipitation = normalise_data(raw_the_amount_of_precipitation)


                yield BaryshivkaMeteoItem(

                            air_temperature=air_temperature,
                            wind_speed=wind_speed,
                            the_amount_of_precipitation=the_amount_of_precipitation
                        )


def normalise_data(data):
    avg_data = None
    data_list = []
    for el in data:
        if el.isdigit():
            data_list.append(float(el))
    try:
        avg_data = sum(data_list) / len(data_list)
    except ZeroDivisionError:
        pass
    return avg_data


def avr_meteo(baryshivka_meteo):
    result = [{}]

    air_temperature = []
    wind_speed = []
    the_amount_of_precipitation = []

    for i in range(len(baryshivka_meteo)):
        if i == 0:
            continue
        air_temperature.append(baryshivka_meteo[i]['air_temperature'])
        wind_speed.append(baryshivka_meteo[i]['wind_speed'])
        the_amount_of_precipitation.append(baryshivka_meteo[i]['the_amount_of_precipitation'])
        
    air_temperature = avr_data(air_temperature)
    wind_speed = avr_data(wind_speed)
    the_amount_of_precipitation = avr_data(the_amount_of_precipitation)

    result[0]['air_temperature'] = air_temperature
    result[0]['wind_speed'] = wind_speed
    result[0]['the_amount_of_precipitation'] = the_amount_of_precipitation
    return result


def avr_data(data):
    data_list = []
    for el in data:
        el = check_data(el)
        data_list.append(el)
    try:
        avg_data = sum(data_list) / len(data_list)
    except ZeroDivisionError:
        return None

    return avg_data


def check_data(data):
    if isinstance(data, str):
        data = data.strip()
        data = data.replace(",", ".")
        data = float(data)
    return data


def get_meteo_baryshivka():
    process = CrawlerProcess()
    process.crawl(SpiderBaryshivkaMeteo)
    process.start()
    


if __name__ == '__main__':
    get_meteo_baryshivka()
