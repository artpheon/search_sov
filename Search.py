from datetime import datetime
from typing import Iterable
from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin, quote
import requests
import re

from numpy import add

class Search():
    def __init__(self):
        self.siteroot = 'https://www.reformagkh.ru/'
        self.search_str = 'search/houses?query='
        self.profile_view = 'myhouse/profile/view/'
        self.profile_passport = 'myhouse/profile/passport/'
    
    def get_view(self, house_id):
        return urljoin(self.siteroot, self.profile_view) + house_id
    
    def get_passport(self, house_id):
        return urljoin(self.siteroot, self.profile_passport) + house_id

    def basic_find_house_id(self, address):
        address_normalized = quote(address)
        url_search = urljoin(self.siteroot, self.search_str) + address_normalized
        soup = self.get_soup_page(url_search)
        cells = soup.find_all('a', {'data-favorite-house-id': re.compile('.*')})
        if len(cells) < 1:
            return None
        else:
            print('<found {} link>'.format(len(cells)))
        house_id = cells[0]['data-favorite-house-id']
        return house_id

    def get_soup_page(self, url):
        page = requests.get(url)
        return BS(page.text, 'html.parser')

    def find_td_data(self, line, page):
        td = page.find_all('td', string=re.compile(rf'.*{line}.*'))
        if len(td) == 0:
            return None
        value = td[0].find_next('td').text.strip()
        if value == 'Не заполнено' or value == '':
            return None
        return value


    def scrape_data_passport(self, page):
        # exploit_year = page.find_all(string="Год ввода дома в эксплуатацию")
        # exploit_year = page.find_all(lambda tag: tag.name=='tr' and "Год ввода дома в эксплуатацию" in tag.string)
        # exploit_year = "NULL" if len(exploit_year) == 0 else exploit_year[0].findNext().text.strip()
        exploit_year = self.find_td_data('Год ввода дома в эксплуатацию', page)

        # floor_num = page.find_all(string="Количество этажей, ед.")
        # floor_num = page.find(lambda tag: tag.name=='tr' and "Количество этажей" in tag.string)
        # floor_num = "NULL" if len(floor_num) == 0 else floor_num[0].findNext().text.strip()
        floor_num = self.find_td_data('Количество этажей', page)
        
        # update_date = page.find_all(string="По данным Фонда ЖКХ информация последний раз актуализировалась:")
        # update_date = page.find(lambda tag: tag.name=='tr' and "По данным Фонда ЖКХ информация последний раз актуализировалась:" in tag.string)
        # update_date = "NULL" if len(update_date) == 0 else update_date[0].findNext().text.strip()
        update_date = datetime.strptime(self.find_td_data('информация последний раз актуализировалась', page), '%d.%m.%Y')

        # building_type = page.find_all(string="Серия, тип постройки здания")
        # building_type = page.find(lambda tag: tag.name=='tr' and "Серия, тип постройки здания" in tag.string)
        # building_type = "NULL" if len(building_type) == 0 else building_type[0].findNext().text.strip()
        building_type = self.find_td_data('тип постройки здания', page)

        # house_type = page.find_all(string="Тип дома")
        # house_type = page.find(lambda tag: tag.name=='tr' and "Тип дома" in tag.string)
        # house_type = "NULL" if len(house_type) == 0 else house_type[0].findNext().text.strip()
        house_type = self.find_td_data('Тип дома', page)

        # is_emergency = page.find_all(string=re.compile(r".*признан аварийным.*"))
        # is_emergency = page.find(lambda tag: tag.name=='tr' and "признан аварийным" in tag.string)
        # is_emergency = "NULL" if len(is_emergency) == 0 else is_emergency[0].findNext().text.strip()
        is_emergency = self.find_td_data('признан аварийным', page)
        is_emergency = True if is_emergency else False

        # cadastral_num = page.find_all(string=re.compile(r".*кадастровый номер.*"))
        # cadastral_num = page.find(lambda tag: tag.name=='tr' and "кадастровый номер" in tag.string)
        # cadastral_num = "NULL" if len(cadastral_num) == 0 else cadastral_num[0].findNext().text.strip()
        cadastral_num = self.find_td_data('Кадастровый номер земельного участка', page)

        floor_type = self.find_td_data('Тип перекрытий', page)

        wall_material = self.find_td_data('Материал несущих стен', page)

        data = {
            'exploit_year': exploit_year,
            'floor_num': floor_num,
            'update_date': update_date,
            'building_type': building_type,
            'house_type': house_type,
            'is_emergency': is_emergency,
            'cadastral_num': cadastral_num,
            'floor_type': floor_type,
            'wall_material': wall_material,
        }
        return data

        

    def scrape_data(self, id):
        link_passport = self.get_passport(id)
        # page_view = self.get_soup_page(link_view)
        page_passport = self.get_soup_page(link_passport)
        # view = self.scrape_data_view(page_view)
        passport = self.scrape_data_passport(page_passport)
        return passport

    def basic(self, address: str):
        house_id = self.basic_find_house_id(address=address)
        if house_id is None:
            return None
        data = self.scrape_data(house_id)
        return data


    def advanced(self, address: Iterable):
        pass

    