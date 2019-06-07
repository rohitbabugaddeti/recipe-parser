import requests
import pprint
import extruct
import validators
from pathlib import Path
import os
headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

#method to check status of url
def is_url_ok(url):
    try:
        return 200 == requests.head(url).status_code
    except Exception:
        return False

def clean_data(data):
    out=[]
    if data['json-ld']!=[]:
        for rec in data['json-ld']:
            if rec['@type'] == 'Recipe':
                d = rec.copy()
                out.append(d)

    if data['microdata'] != []:
        for rec in data['microdata']:
            if rec['type'] in ('http://schema.org/Recipe',
                               'https://schema.org/Recipe'):
                d = rec['properties'].copy()
                #@context and @type to match json-ld style
                if rec['type'][:6] == 'https:':
                    d['@context'] = 'https://schema.org'
                else:
                    d['@context'] = 'http://schema.org'
                d['@type'] = 'Recipe'

                for key in d.keys():
                    if isinstance(d[key], dict) and 'type' in d[key]:
                        type_ = d[key].pop('type')
                        d[key]['@type'] = type_.split('/')[3] #taking last part of url which holds type

                out.append(d)

    return out

def parse_from_url(url):
    if not isinstance(url,str):
        raise TypeError
    good_data={}
    if(is_url_ok(url)):
        response = requests.get(url, headers=headers)
        data = extruct.extract(response.text, response.url)
        good_data=clean_data(data)
    else:
        print('URL may be Dead/Not Working !')

    return good_data

def parse(obj):
    if isinstance(obj,str): #if it is str object
        if validators.url(obj): #if it is url
            return parse_from_url(obj)
        else: #it is file path
            with open(obj, 'rt') as f:
               data=extruct.extract(f.read())

    elif hasattr(obj,'read'): #if it is and object with read attribute
        data=extruct.extract(obj.read())
    elif isinstance(obj,Path): #if it is a path instance
        with obj.open(mode='rt') as fobj:
            data=extruct.extract(fobj.read())
    else:
        raise TypeError('unexpected type encountered') #unexpected type
    out = clean_data(data)
    return out

def test_parse():
    dirname = os.path.dirname(__file__)
    arg = Path(dirname + '/bevvy-irish-coffee.html')
    pprint.pprint(parse(arg))
    print('---------------------------------------')
    f = open(arg, 'rt')
    pprint.pprint(parse(f))
    f.close()
    print('-------------------------------')
    arg = 'https://www.foodnetwork.com/recipes/alton-brown/honey-mustard-dressing-recipe-1939031'
    pprint.pprint(parse(arg))

    print('------------------------------')
    pprint.pprint(parse('D:/GitHub/recipe-parser/bevvy-irish-coffee.html'))


test_parse()