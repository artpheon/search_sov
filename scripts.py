from DBModels import get_session, SearchRequest, SearchResponse

def found_statistics():
    s = get_session()
    found = s.query(SearchResponse).count
    all = s.query(SearchRequest).count
    not_found = all - found
    print('<statistics>\nAll search requests: {}\nFound: {}\nNot found: {}'.format(all, found, not_found))
