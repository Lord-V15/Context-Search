import elasticsearch
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def es_search(search_term,prices,brand,rating,shipping,colour,latest):
    # AVAILABLE FILTERS : BRAND, COLOUR, FREE SHIPPING, RATING & PRICE RANGE
    filters = []
    if prices['gte_flag']:
        filters.append({ "range": { "price": { "gte": prices['gte_amount'] }}})
    if prices['lte_flag']:
        filters.append({ "range": { "price": { "lte": prices['lte_amount'] }}})
    if brand is not None :
        filters.append({ "match": { "brand": brand }})
    if rating is not None :
        filters.append({ "term": { "rating": rating }})
    if shipping is not None :
        filters.append({ "term": { "free_shipping": True }})
        
    musts = [{ "match": {"name": search_term} }]
    if colour is not None:
        musts.append({ "match": {"name": colour} })
    if latest is not None:
        musts.append({ "match": {"name": latest} })
    # if [brand, colour, shipping, rating, latest] == [None, None, None, None, None]:
    #     musts.append({ "match": {"description": search_term}})
    body = {"query": {"bool": {"must": musts, # to show must needed results
                           "filter": filters # to show relevant results
                           }     }    }  
    res = es.search(index='zevi', body=body)
    output = []
    for doc in res['hits']['hits']:
        output.append(doc)
    return output
