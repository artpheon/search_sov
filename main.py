import pandas as pd
from DBModels import get_session, drop_tables, SearchRequest
from process import process
import os


def fill_db(tb):
    s = get_session()
    res = 0
    for i in range(0, len(tb)):
        data = tb.iloc[i].to_dict()
        # replacing NaN from the table cells with None
        s.add(SearchRequest(**dict((k, v) for k, v in data.items() if v == v)))
        s.commit()
        res += 1
    s.close()
    return res


if __name__ == "__main__":
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/Test.xlsx")
    test_table = pd.read_excel(path, dtype=str)
    drop_tables()
    print("Filling in the database...")
    added = fill_db(test_table)
    print(f"Successfully filled {added} entries to search")
    print("Starting monitoring the search requests...")
    process()
