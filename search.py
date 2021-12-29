from typing import Iterable
import pandas as pd

class Search():
    def __init__(self, table='/home/hrobbin/python/search_sov/src/Test.xlsx', index=0) -> None:
        self.table = pd.read_excel(table)
        self.data = self.table.iloc[index].to_dict()
        self.basic_addr_str = self.data['Adress']
        self.advanced_addr = {
            'region': self.data['Adress_Region'],
            'settlement': self.data['']
        }

    def basic(address: str):
        pass

    def advanced(address: Iterable):
        pass

    