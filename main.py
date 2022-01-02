from re import search
from requests.api import get
from Search import Search
import pandas as pd
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Insert
from sqlalchemy import create_engine
from DBModels import get_session, SearchRequest, SearchResponse

# @compiles(Insert)
# def _prefix_insert_with_ignore(insert, compiler, **kw):
#     return compiler.visit_insert(insert.prefix_with('IGNORE'), **kw)

# sql_table = "{}.{}".format(data['schema'], data['table_site_reports'])

def make_basic_addr(data):
    addr = ""
    if data['Adress_Region'] == data['Adress_Region']:
        addr += data['Adress_Region'] + ', '
    if data['Adress_City'] == data['Adress_City']:
        addr += data['Adress_City'] + ', '
    if data['Adress_Street'] == data['Adress_Street']:
        addr += data['Adress_Street'] + ', '
    if data['Adress_House'] == data['Adress_House']:
        addr += data['Adress_House']
    if data['Adress_Block'] == data['Adress_Block']:
        addr += ', ' + data['Adress_Block']
    return addr

def test_many(table):
    search = Search()
    with open('data.log', 'w') as f:
        for i in range(0, len(table)):
            data = table.iloc[i].to_dict()
            print(f'<address unformatted>\n{data}')
            basic_addr_str = make_basic_addr(data)
            print(f'<searching address:>\n{basic_addr_str}')
            info = search.basic(basic_addr_str)
            print(info)
            f.write(info.__str__())
            f.write('\n')

def fill_db(table):
    s = get_session()
    for i in range(0, len(table) // 2):
        data = table.iloc[i].to_dict()
        
        s.add(SearchRequest(**dict((k,v) for k, v in data.items() if v == v)))
        print(f'<address unformatted>\n{data}')
        basic_addr_str = make_basic_addr(data)
        print(f"address formatted\n{basic_addr_str}")
        # print(f'<searching address:>\n{basic_addr_str}')
        # print(info)
    s.commit()
    s.close()
    


path ='/home/hrobbin/python/search_sov/src/Test.xlsx'
index=1
table = pd.read_excel(path, dtype=str)
data = table.iloc[index].to_dict()
basic_addr_str = make_basic_addr(data)
# test_many(table)
# fill_db(table)