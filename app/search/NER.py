import re
from monkeylearn import MonkeyLearn

def NER(query):
    ml = MonkeyLearn('c2cf077e8886eecf879de6fff30e1f72b38652ef')
    model_id = 'ex_sUxkptEt'
    data = [query]
    response = ml.extractors.extract(model_id, data=data)
    return response

def is_float(n):
    try:
        float(n)
    except ValueError:
        return False
    return True
    
def is_int(n):
    try:
        int(n)
    except ValueError:
        return False
    return True

def amount(string):
    for i in string.split():
        if "$" or " $" in i :  # Find '$' in query
            i=i.replace("$","")
            return i
            break
        elif is_float(string.split()[0]) or is_int(string.split()[0]):
            return string.split()[0]
        else :
            return None
        
def price_filter(string):        
    greater = ['more than','above','over','higher than'] # filter keywords
    smaller = ['less than','below','under','lower than'] # filter keywords
    lte, gte, lte_amount, gte_amount=False, False, None, None
    for i in string.split() :
        for j in greater:
            if i == j : # if keyword found in query
                gte = True
                pos = re.search(i,string).span() # Search for position of keyword
                gte_amount = amount(string[pos[1]:]) # Find amount ahead of the keyword 
                break
        for j in smaller :
            if i == j : # if keyword found in query
                lte = True
                pos = re.search(i,string).span() # Search for position of keyword
                lte_amount = amount(string[pos[1]:]) # Find amount ahead of the keyword 
                break
    return { 'gte_flag':gte, 'gte_amount':gte_amount, 'lte_flag':lte, 'lte_amount':lte_amount}
