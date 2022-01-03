from DBModels import get_session, SearchRequest, SearchResponse
from time import sleep
from Search import Search


def make_search_string(query):
    string = [
        query.Adress_Region,
        query.Adress_City,
        query.Adress_Street,
        query.Adress_House,
        query.Adress_Block,
    ]
    string = [s for s in string if s is not None]
    return ", ".join(string)


def process():
    search = Search()
    s = get_session()
    while True:
        # looking for not-searched queries
        queries = s.query(SearchRequest).filter(SearchRequest.is_searched == False)
        for query in queries:
            search_string = make_search_string(query)
            print(f"looking for {search_string}")
            result = search.basic(search_string)
            query.is_searched = True
            if result is None:
                print("not found")
            else:
                # binding the request id to the result
                d = {"request_id": query.id} | result
                s.add(SearchResponse(**d))
            s.commit()
        sleep(5)


if __name__ == "__main__":
    process()
