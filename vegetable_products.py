import requests
import base64
import os
import json
from dotenv import load_dotenv
from product_info_from_request import extract_product_info
from avg_weight_vegetables import get_avg_weight

load_dotenv()

def load_secrets():
    client_id = os.environ.get("client_id")
    client_secret = os.environ.get("client_secret")
    encoded = bytes((client_id + ':' + client_secret), encoding='utf8')
    return base64.b64encode(encoded)

def get_refresh_token():

    encoded = load_secrets()

    base_url = os.environ.get("base_url")
    url = base_url + 'connect/oauth2/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': b'Basic '+ encoded}
    params = {
        'scope': 'product.compact'
    }
    data = 'grant_type=refresh_token'

    response = requests.post(url, headers=headers, params=params, data=data)
    token = response.json()['access_token']
    return token

def extract_all_vegetable_products(location):

    encoded = load_secrets()

    # generate token to access API
    base_url = os.environ.get("base_url")
    url = base_url + 'connect/oauth2/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': b'Basic '+ encoded}
    params = {
        'scope': 'product.compact'
    }
    data = 'grant_type=client_credentials'

    response = requests.post(url, headers=headers, params=params, data=data)
    token = response.json()['access_token']
          
    url = base_url + 'products'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    params = {
        'filter.term': 'vegetable',
        'filter.locationId': location
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 401:
        token = get_refresh_token()
    
    url = base_url + 'products'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    
    response = requests.get(url, headers=headers, params=params)
    cnt = 0

    while response.status_code == 200:
        url = base_url + 'products'
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }
        params = {
            'filter.term': 'vegetable',
            'filter.locationId': location,
            'filter.start': 1 + 50*cnt,
            'filter.limit': 50
        }
        cnt += 1
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200 and cnt == 1:
            raw = response.json()['data']
            vegetable_products = extract_product_info(raw)
        elif response.status_code == 200:
            raw = response.json()['data']
            vegetable_products = vegetable_products.append(extract_product_info(raw))

    # post-processing of a complete list of vegetable products
    vegetable_products = vegetable_products[vegetable_products['categories']=='Produce']
    vegetable_products = vegetable_products.drop_duplicates()
    vegetable_products['description'] = vegetable_products['description'].str.lower()
    vegetable_products = vegetable_products[~vegetable_products['description'].str.contains('bowl')]
    vegetable_products[['weight', 'weight_unit']] = vegetable_products['size'][~vegetable_products['size'].str.contains('/')].str.split(' ', expand = True)
    vegetable_products['weight'][vegetable_products['size'] == 'each'] = 1
    vegetable_products['weight_unit'][vegetable_products['size'] == 'each'] = 'ct'
    vegetable_products['size'][vegetable_products['size'] == 'each'] = 'NaN'
    vegetable_products['weight'] = vegetable_products['weight'].astype('float64')
    ## new: filter out produce in which weight_in_lb is not available (cannot compare or estimate)
    vegetable_products = vegetable_products.reset_index(level=None, drop=True)
    vegetable_products['weight_in_lb'] = vegetable_products['weight'][(vegetable_products['weight_unit'] == 'oz')]*0.0625
    vegetable_products['weight_in_lb'] = vegetable_products['weight_in_lb'].fillna(vegetable_products['weight'][vegetable_products['weight_unit'] == 'lb'])
    vegetable_products = vegetable_products[~vegetable_products['weight_in_lb'].isna()]
    vegetable_products['lowest_price'] = vegetable_products['price_promo'].fillna(vegetable_products['price_regular']).astype('float64')
    vegetable_products['lowest_price_per_lb'] = vegetable_products['lowest_price']/vegetable_products['weight_in_lb']
    vegetable_products.sort_values(by='lowest_price_per_lb')
    return vegetable_products

def extract_vegetable_products(vegetable_products):
    # vegetable_products = extract_all_vegetable_products(location)
    vegetable_list = vegetable_products['description'].tolist()[0:3]
    return vegetable_list

def extract_cheapest_vegetable_products(vegetable_products):
    # vegetable_products = extract_all_vegetable_products(location)
    vegetable_list = vegetable_products['description'].tolist()[0:1]
    return vegetable_list

#####
    # get weight reference for each vegetable
    # weight_reference = get_avg_weight()
    # ref_list = weight_reference['vegetable_type'].tolist()
    # X_dict = {}
    # for ref in ref_list:
    #     for veg in vegetables:
    #         if veg in ref:
    #             X_dict[veg] = weight_reference['weight_per_lb'][weight_reference['vegetable_type'] == ref].item()
    #         else:
    #             X_dict[veg] = 'NaN'
    # vegetable_products['weight_per_ct'] = vegetable_products['description'].map(X_dict)
#####