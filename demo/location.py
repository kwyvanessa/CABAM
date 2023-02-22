import requests
import base64
import os
import json
from dotenv import load_dotenv
load_dotenv()

def extract_location_info(X):

    # load secrets
    client_id = os.environ.get("client_id")
    client_secret = os.environ.get("client_secret")
    base_url = os.environ.get("base_url")
    encoded = bytes((client_id + ':' + client_secret), encoding='utf8')
    encoded = base64.b64encode(encoded)

    # generate token to access API
    url = base_url + 'connect/oauth2/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': b'Basic '+ encoded}
    params = {
        'scope': 'product.compact'
    }
    data = 'grant_type=client_credentials'

    response = requests.post(url, headers=headers, params=params, data=data)
    token = response.json()['access_token']

    zip_code = str(X)
    url = base_url + 'locations'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    params = {
        'filter.zipCode.near': zip_code, # user's input 
        'filter.department': '88', # name: 'Perishables'
    }
    response = requests.get(url, headers=headers, params=params)

    if len(response.json()['data']) != 0:
        location_and_info = []
        location_and_info = response.json()['data'][0]
        location = 'Store name: ' + location_and_info['chain']
        address = 'Address: ' + location_and_info['address']['addressLine1'] + ', ' + location_and_info['address']['city'] + ', ' + location_and_info['address']['state'] + ', ' + location_and_info['address']['zipCode'] + ', ' + location_and_info['address']['county']
        return (location + '\n' + address)
    else: 
        return "Sorry! There is no location close to you."

def extract_store_location_id(X):

    # load secrets
    client_id = os.environ.get("client_id")
    client_secret = os.environ.get("client_secret")
    base_url = os.environ.get("base_url")
    encoded = bytes((client_id + ':' + client_secret), encoding='utf8')
    encoded = base64.b64encode(encoded)

    # generate token to access API
    url = base_url + 'connect/oauth2/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': b'Basic '+ encoded}
    params = {
        'scope': 'product.compact'
    }
    data = 'grant_type=client_credentials'

    response = requests.post(url, headers=headers, params=params, data=data)
    token = response.json()['access_token']

    zip_code = str(X)
    url = base_url + 'locations'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    params = {
        'filter.zipCode.near': zip_code, # user's input 
        'filter.department': '88', # name: 'Perishables'
    }
    response = requests.get(url, headers=headers, params=params)
    if len(response.json()['data']) != 0:
        return response.json()['data'][0]['locationId']
