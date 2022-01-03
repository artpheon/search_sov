from DBModels import get_engine, get_session, SearchRequest, SearchResponse
from sqlalchemy import text
from sys import argv


def get_res_from_query(sql_query):
    e = get_engine("artur", "1234", "localhost", "5432", "search_gkh")
    sql = text(sql_query)
    result = e.execute(sql)
    return [r for r in result]


def found_statistics():
    s = get_session()
    found_queries = s.query(SearchResponse).count()
    all_queries = s.query(SearchRequest).count()
    not_found_queries = all_queries - found_queries
    return {
        "all_queries": all_queries,
        "found_queries": found_queries,
        "not_found_queries": not_found_queries,
    }


def material_statistics():
    result = get_res_from_query(
        '''select "Adress_Region" as region, count(*) as num_of_houses
from search_response as res
join search_requests as req
on res.request_id = req.id
where wall_material in ('Кирпич', 'Кирпичный')
group by "Adress_Region"'''
    )
    return result


def max_floors():
    result = get_res_from_query(
        """
select * from (select max("floor_num") as floors, "Adress_City" as "city", "Adress_Region" as "region", "wall_material" as "material"
    from search_requests as req
            join search_response as res on req.id=res.request_id
    group by "Adress_City", "wall_material", "Adress_Region"
    order by "Adress_City") items
where floors is not null and material is not null;"""
    )
    return result


if __name__ == "__main__":
    if len(argv) == 1:
        print(
            "Use 'script.py 1' to get search statistics, 'script.py 2' to get statistics about wall material, 'script.py 3' to get statistics of maximum floor number"
        )
    elif argv[1] == "1":
        print(found_statistics())
    elif argv[1] == "2":
        print(material_statistics())
    elif argv[1] == "3":
        print(max_floors())
