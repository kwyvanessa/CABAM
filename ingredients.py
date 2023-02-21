import requests
import os
import json
from dotenv import load_dotenv
import pandas as pd
from ingredient_parser import parse_multiple_ingredients
from ingredient_parser import parse_ingredient

load_dotenv()
# load secrets
# key = os.environ.get("X-RapidAPI-Key")
# host = os.environ.get("X-RapidAPI-Host")
app_id = os.environ.get("app_id")
app_key = os.environ.get("app_key")

def parsed_ingredients_list_to_dataframe(X):
    column_names = [
        'name', 'quantity', 'unit', 'food_category', 'recipe_weight_in_grams', 'recipe_weight_in_lb'
                   ]
    df = pd.DataFrame(X, columns = column_names)
    
    for column in column_names:
        temp_data = []
        for row in range(len(X)):
            if column in X[row] and len(X[row][column]) !=0:
                temp_data.append(X[row][column].lower())
            else: 
                temp_data.append('NaN')
        df[column] = temp_data
    return df

def dict_with_item_and_food_category_and_weight(X):
    X_dict = {}
    for i in range(len(X)):
        item = parse_ingredient(X[i]['text'])['name'].lower()
        food_category = X[i]['foodCategory'].lower()
        X_dict[item] = food_category
    Y_dict = {}
    for i in range(len(X)):
        item = parse_ingredient(X[i]['text'])['name'].lower()
        weight = X[i]['weight']
        Y_dict[item] = weight 
    return X_dict, Y_dict

def add_food_category_to_df(X,Y):
    X_dict, Y_dict = dict_with_item_and_food_category_and_weight(Y)
    for key in X_dict:
        ind = X.index[X['name'] == key].tolist()
        X['food_category'][ind] = X_dict[key]
    for key in Y_dict:
        ind = X.index[X['name'] == key].tolist()
        X['recipe_weight_in_grams'][ind] = Y_dict[key]
        X['recipe_weight_in_lb'][ind] = Y_dict[key]*0.00220462
    return X

def prepare_ingredients_table(ingredient, recipe_idx, portion):

    # url = "https://edamam-recipe-search.p.rapidapi.com/search"
    # headers = {
    #     "X-RapidAPI-Key": key,
    #     "X-RapidAPI-Host": host
    # }
    # params = {"q": ingredient} # put only the main ingredient
    # response = requests.get(url, headers=headers, params=params)

    start = str(0)
    end = str(recipe_idx+1)
    url = "https://api.edamam.com/search?q=" + ingredient + "&app_id=" + app_id + "&app_key=" + app_key + "&from=" + start + "&to=" + end
    response = requests.get(url)
    recipe_yield = response.json()['hits'][recipe_idx]['recipe']['yield']
    detailed_list_of_ingredients = response.json()['hits'][recipe_idx]['recipe']['ingredients']
    list_of_ingredients = response.json()['hits'][recipe_idx]['recipe']['ingredientLines']
    parsed_list_of_ingredients = parse_multiple_ingredients(list_of_ingredients)
    df_ingredients_list = parsed_ingredients_list_to_dataframe(parsed_list_of_ingredients)
    df_ingredients_list = add_food_category_to_df(df_ingredients_list, detailed_list_of_ingredients)
    df_ingredients_list['recipe_yield'] = recipe_yield
    df_ingredients_list['preferred_yield'] = portion 

    return df_ingredients_list

def get_recipe_url(ingredient, recipe_idx):

    # url = "https://edamam-recipe-search.p.rapidapi.com/search"
    # headers = {
    #     "X-RapidAPI-Key": key,
    #     "X-RapidAPI-Host": host
    # }
    # params = {"q": ingredient} # put only the main ingredient

    start = str(0)
    end = str(recipe_idx+1)
    url = "https://api.edamam.com/search?q=" + ingredient + "&app_id=" + app_id + "&app_key=" + app_key + "&from=" + start + "&to=" + end
    response = requests.get(url)

    recipe_url = response.json()['hits'][recipe_idx]['recipe']['url']

    return recipe_url

# def prepare_ingredients_table(X, Y, Z):
#     ingredient = X
#     recipe_idx = Y
#     portion = Z

#     url = "https://edamam-recipe-search.p.rapidapi.com/search"
#     headers = {
#         "X-RapidAPI-Key": key,
#         "X-RapidAPI-Host": host
#     }
#     params = {"q": ingredient} # put only the main ingredient
#     response = requests.get(url, headers=headers, params=params)
#     recipe_yield = response.json()['hits'][recipe_idx]['recipe']['yield']
#     detailed_list_of_ingredients = response.json()['hits'][recipe_idx]['recipe']['ingredients']
#     list_of_ingredients = response.json()['hits'][recipe_idx]['recipe']['ingredientLines']
#     parsed_list_of_ingredients = parse_multiple_ingredients(list_of_ingredients)
#     df_ingredients_list = parsed_ingredients_list_to_dataframe(parsed_list_of_ingredients)
#     df_ingredients_list = add_food_category_to_df(df_ingredients_list, detailed_list_of_ingredients)
#     df_ingredients_list['recipe_yield'] = recipe_yield
#     df_ingredients_list['preferred_yield'] = portion 

#     return df_ingredients_list
