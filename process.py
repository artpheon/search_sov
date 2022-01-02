from requests.api import get
from DBModels import get_session, SearchRequest, SearchResponse
from time import sleep
from Search import Search


def make_search_string(query):
    string = [query.Adress_Region, query.Adress_City, query.Adress_Street, query.Adress_House, query.Adress_Block]
    string = [s for s in string if s is not None]
    return ", ".join(string)


def process():
    while True:
        s = get_session()
        queries = s.query(SearchRequest).filter(SearchRequest.is_searched==False)
        search = Search()
        for query in queries:
            search_string = make_search_string(query)
            result = search.basic(search_string)
            query.is_searched = True
            if result is None:
                pass
            else:
                d = { "request_id": query.id } | result
                print(f'<searched a request>\nreq id:{d["request_id"]}')
                s.add(SearchResponse(**d))
            s.commit()
        sleep(5)

process()