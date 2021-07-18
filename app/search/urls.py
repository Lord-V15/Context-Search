"""
/* urls.py - APIs' URLs for contextual search app */

/* Copyright (c) 2021, Vibhansh Gupta*/
/*
modification history
--------------------
01a,18jul21,lord written.
"""

from fastapi import APIRouter, HTTPException, Depends
import json
import timeit
from pydantic import BaseModel

from .preprocessing import preprocess
from .NER import NER, is_float, is_int, amount, price_filter
from .search import es_search

router = APIRouter()

class Query(BaseModel):
    user_query: str
@router.post("/contextual_search")
def intelligent_search_using_NER(item: Query):

    query = item.user_query
    
    start = timeit.default_timer()
    search_term = query
    prices = price_filter(query) # Detect Price
    stop = timeit.default_timer()
    print('Time to extract prices :  ', stop - start)
    
    start = timeit.default_timer()
    response = NER(query)
    stop = timeit.default_timer()
    print('Time taken to run NER :  ', stop - start)
    
    start = timeit.default_timer()
    brand, colour, shipping, rating = None, None, None, None
    for i in response.body[0]['extractions']:
        search_term = search_term.replace(i['extracted_text'],"") 
        # Save every entity if found
        if i['tag_name']=='Brand':
            brand=i['extracted_text']
        elif i['tag_name']=='Colour':
            colour=i['extracted_text']
        elif i['tag_name']=='Shipping':
            shipping=i['extracted_text']
        elif i['tag_name']=='Rating':
            rating=i['extracted_text'][0]
    if prices['gte_flag']:
        search_term = search_term.replace(prices['gte_amount']+"$","")
    if prices['lte_flag']:
        search_term = search_term.replace(prices['lte_amount']+"$","")
    search_term = preprocess(search_term, stopword=True)
    stop = timeit.default_timer()
    print('Time taken to get Search Terms :  ', stop - start)
    
    start = timeit.default_timer()
    output = es_search(search_term,prices,brand,rating,shipping,colour)
    stop = timeit.default_timer()
    print('Time to get results :  ', stop - start)
    
    return output