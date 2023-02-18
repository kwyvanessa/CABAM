import requests
import os
import json
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
# load secrets
key = os.environ.get("X-RapidAPI-Key")
host = os.environ.get("X-RapidAPI-Host")

def convert_detailed_nutritional_value_to_df(X):
    column_names = ['label', 'total', 'hasRDI','daily','unit']
    df = pd.DataFrame(X, columns = column_names)
    for i in range(len(X)):
        X_dict_keys = X[i].keys()
        if 'sub' in X_dict_keys:
            for ind in range(len(X[i]['sub'])):
                new_X_dict = {}
                new_label = X[i]['sub'][ind]['label'] + ' ' + X[i]['label']
                new_X_dict['label'] = new_label
                new_X_dict['total'] = X[i]['sub'][ind]['total']
                new_X_dict['hasRDI'] = X[i]['sub'][ind]['hasRDI']
                new_X_dict['daily'] = X[i]['sub'][ind]['daily']
                new_X_dict['unit'] = X[i]['sub'][ind]['unit']
                df = df.append([new_X_dict], ignore_index=True)
    return df
    
def calculate_nutrition_score_for_each_recipe(ingredient):
    # TODO: implement for loop to get ALL recipes

    url = "https://edamam-recipe-search.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": host
    }
    params = {"q": ingredient,} # put only the main ingredient

    response = requests.get(url, headers=headers, params=params)
    upper_limit = response.json()['count']
    more = response.json()['more']

    df = pd.DataFrame(columns = ['recipe_id', 'recipe_name', 'nutrition_score'], index=None)
    cnt = 1 #0 

    for interval in range(0, upper_limit+1, 10):
        params = {
            "q": ingredient,
            "from": 1 + interval,
            "to": 10 + interval
            }
        response = requests.get(url, headers=headers, params=params)
        more = response.json()['more']
        while more == 'True':
            for i in range(len(response.json()['hits'])):
                cnt += 1
                recipe_name = response.json()['hits'][i]['recipe']['label']
                recipe_yield = response.json()['hits'][i]['recipe']['yield']
                detailed_nutritional_value = response.json()['hits'][i]['recipe']['digest']
                df_detailed_nutritional_value = convert_detailed_nutritional_value_to_df(detailed_nutritional_value)
                df_detailed_nutritional_value[['total', 'daily']] = df_detailed_nutritional_value[['total', 'daily']]/recipe_yield
                df_detailed_nutritional_value['DV(%)'] = df_detailed_nutritional_value['total']/df_detailed_nutritional_value['daily']*100
                df_detailed_nutritional_value['DV(%)'] = df_detailed_nutritional_value['DV(%)'].replace(float('NaN'),'0')
                df_detailed_nutritional_value['DV(%)'] = df_detailed_nutritional_value['DV(%)'].replace(float('inf'),'-1')
                df_detailed_nutritional_value['DV(%)'] = df_detailed_nutritional_value['DV(%)'].astype('float64')
                nutrition_score = 0
                nutrition_score += df_detailed_nutritional_value['DV(%)'][(df_detailed_nutritional_value['DV(%)'] > 0) & (df_detailed_nutritional_value['DV(%)'] < 20)].count()*1
                nutrition_score += df_detailed_nutritional_value['DV(%)'][(df_detailed_nutritional_value['DV(%)'] >=20) & (df_detailed_nutritional_value['DV(%)'] < 40)].count()*2
                nutrition_score += df_detailed_nutritional_value['DV(%)'][(df_detailed_nutritional_value['DV(%)'] >=40) & (df_detailed_nutritional_value['DV(%)'] < 60)].count()*3
                nutrition_score += df_detailed_nutritional_value['DV(%)'][(df_detailed_nutritional_value['DV(%)'] >=60) & (df_detailed_nutritional_value['DV(%)'] < 80)].count()*4
                nutrition_score += df_detailed_nutritional_value['DV(%)'][(df_detailed_nutritional_value['DV(%)'] >=80) & (df_detailed_nutritional_value['DV(%)'] < 100)].count()*5
                nutrition_score += df_detailed_nutritional_value['DV(%)'][(df_detailed_nutritional_value['DV(%)'] >=100)].count()*-1
                nutrition_score += df_detailed_nutritional_value['DV(%)'][(df_detailed_nutritional_value['DV(%)'] == -1)].count()*-1
                X_dict = {}
                X_dict['recipe_id'] = cnt
                X_dict['recipe_name'] = recipe_name
                X_dict['nutrition_score'] = nutrition_score
                df = df.append([X_dict], ignore_index=True)
    df = df.sort_values(by='nutrition_score', ascending=False)
    df = df.set_index('recipe_id')
    return df

