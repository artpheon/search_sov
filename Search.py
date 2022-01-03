from datetime import datetime
from typing import Iterable
from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin, quote
import requests
import re


class Search:
    def __init__(self):
        self.siteroot = "https://www.reformagkh.ru/"
        self.search_str = "search/houses?query="
        self.profile_passport = "myhouse/profile/passport/"

    def get_passport(self, house_id):
        return urljoin(self.siteroot, self.profile_passport) + house_id

    def basic_find_house_id(self, address):
        address_normalized = quote(address)
        url_search = urljoin(self.siteroot, self.search_str) + address_normalized
        soup = self.get_soup_page(url_search)
        cells = soup.find_all("a", {"data-favorite-house-id": re.compile(".*")})
        if len(cells) < 1:
            return None
        house_id = cells[0]["data-favorite-house-id"]
        return house_id

    def get_soup_page(self, url):
        page = requests.get(url)
        return BS(page.text, "html.parser")

    def find_td_data(self, line, page):
        td = page.find_all("td", string=re.compile(rf".*{line}.*"))
        if len(td) == 0:
            return None
        value = td[0].find_next("td").text.strip()
        if value == "Не заполнено" or value == "":
            return None
        return value

    def scrape_data_passport(self, page):
        exploit_year = self.find_td_data("Год ввода дома в эксплуатацию", page)

        floor_num = self.find_td_data("Количество этажей", page)

        update_date = self.find_td_data(
            "информация последний раз актуализировалась", page
        )
        update_date = (
            None if update_date is None else datetime.strptime(update_date, "%d.%m.%Y")
        )

        building_type = self.find_td_data("тип постройки здания", page)

        house_type = self.find_td_data("Тип дома", page)

        is_emergency = self.find_td_data("признан аварийным", page)
        is_emergency = True if is_emergency else False

        cadastral_num = self.find_td_data("Кадастровый номер земельного участка", page)

        floor_type = self.find_td_data("Тип перекрытий", page)

        wall_material = self.find_td_data("Материал несущих стен", page)

        data = {
            "exploit_year": exploit_year,
            "floor_num": floor_num,
            "update_date": update_date,
            "building_type": building_type,
            "house_type": house_type,
            "is_emergency": is_emergency,
            "cadastral_num": cadastral_num,
            "floor_type": floor_type,
            "wall_material": wall_material,
        }
        return data

    def scrape_data(self, id):
        link_passport = self.get_passport(id)
        page_passport = self.get_soup_page(link_passport)
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
