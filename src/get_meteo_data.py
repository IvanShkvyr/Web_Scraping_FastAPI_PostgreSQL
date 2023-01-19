import json
from multiprocessing import Process

from src.service_config import BASE_DIR
from src.spiders import get_meteo_baryshivka, get_meteo_odesa, get_meteo_rivne


file_link_odesa = BASE_DIR / 'src' / 'spiders' / 'odesa_meteo.json'
file_link_rivne = BASE_DIR / 'src' / 'spiders' / 'rivne_meteo.json'
file_link_baryshivka = BASE_DIR / 'src' / 'spiders' / 'baryshivka_meteo.json'

def get_unite_data(odesa_data, rivne_data, baryshivka_data):

    meteo_data = {}

    meteo_data['odesa_air_temp'] = odesa_data[0]["air_temperature"]
    meteo_data['odesa_wind_spd'] = odesa_data[0]["wind_speed"]
    meteo_data['odesa__prc'] = odesa_data[0]["the_amount_of_precipitation"]
    meteo_data['rivne_air_temp'] = rivne_data[0]["air_temperature"]
    meteo_data['rivne_wind_spd'] = rivne_data[0]["wind_speed"]
    meteo_data['rivne__prc'] = rivne_data[0]["the_amount_of_precipitation"]
    meteo_data['baryshivka_air_temp'] = baryshivka_data[0]["air_temperature"]
    meteo_data['baryshivka_wind_spd'] = baryshivka_data[0]["wind_speed"]
    meteo_data['baryshivka_prc'] = baryshivka_data[0]["the_amount_of_precipitation"]

    return meteo_data


def main():
    pr1 = Process(target=get_meteo_baryshivka.get_meteo_baryshivka)
    pr2 = Process(target=get_meteo_odesa.get_meteo_odesa)
    pr3 = Process(target=get_meteo_rivne.get_meteo_rivne)

    pr1.start()
    pr2.start()
    pr3.start()

    pr1.join()
    pr2.join()
    pr3.join()

    with open(file_link_odesa, 'r', encoding='utf-8') as fd:
        odesa_data = json.load(fd)

    with open(file_link_rivne, 'r', encoding='utf-8') as fd:
        rivne_data = json.load(fd)

    with open(file_link_baryshivka, 'r', encoding='utf-8') as fd:
        baryshivka_data = json.load(fd)

    result = get_unite_data(odesa_data, rivne_data, baryshivka_data)
    return(result)
    

if __name__ == '__main__':

    print(main())


