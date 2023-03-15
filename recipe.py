import requests
import os
import json
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
# load secrets
# key = os.environ.get("X-RapidAPI-Key")
# host = os.environ.get("X-RapidAPI-Host")
app_id = os.environ.get("app_id")
app_key = os.environ.get("app_key")

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

    start = str(0)
    end = str(100)
    url = "https://api.edamam.com/search?q=" + ingredient + "&app_id=" + app_id + "&app_key=" + app_key + "&from=" + start + "&to=" + end
    response = requests.get(url)
    more = response.json()['more']

    df = pd.DataFrame(columns = ['recipe_id', 'recipe_name', 'nutrition_score'], index=None)

    interval = 0

    while response.status_code == 200 and more == bool('True') and len(response.json()['hits']) > 0:
        start = str(0 + 100*interval)
        end = str(100 + 100*interval)
        url = "https://api.edamam.com/search?q=" + ingredient + "&app_id=" + app_id + "&app_key=" + app_key + "&from=" + start + "&to=" + end
        response = requests.get(url)
        more = response.json()['more']
        interval += 1
        if response.status_code == 200 and more == bool('True') and len(response.json()['hits']) > 0:
            for i in range(len(response.json()['hits'])):
                health_labels = [i.lower() for i in response.json()['hits'][i]['recipe']['healthLabels']]
                #include only vegetarian recipes and main course
                if 'vegetarian' in health_labels:
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
                    X_dict['recipe_id'] = i 
                    X_dict['recipe_name'] = recipe_name
                    X_dict['nutrition_score'] = nutrition_score
                    df = df.append([X_dict], ignore_index=True)
    df = df.sort_values(by='nutrition_score', ascending=False)
    return df

