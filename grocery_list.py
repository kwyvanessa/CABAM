import pandas as pd
import numpy as np
import nltk 
nltk.download('averaged_perceptron_tagger') 

from product_info_from_request import extract_product_info
from vegetable_products import extract_all_vegetable_products
from ingredients import prepare_ingredients_table

IGNORE_GROCERY_COLS = ['categories','itemId','favorite','fulfillment_curbside','fulfillment_delivery','fulfillment_inStore','fulfillment_shipToHome','weight','weight_unit']

def get_grocery_list(vegetable_products, ingredient, recipe_idx, portion):
    #find cheapest price for groceries needed
    df_ingredients_table = prepare_ingredients_table(ingredient, recipe_idx, portion)
    description_list = df_ingredients_table['name'].tolist()
    description_list = [i.split() for i in description_list]
    alt_description_list = []
    for ingredients in description_list:
        sorted_ingredients = sorted(ingredients)
        new_string = " ".join(sorted_ingredients)
        alt_description_list.append(new_string)
    df_ingredients_table['sorted_name'] = alt_description_list
    ingredients_search = df_ingredients_table['sorted_name'][df_ingredients_table['food_category']=='vegetables'].tolist()
    df_vegetable_products = vegetable_products
    description_list = df_vegetable_products['description'].tolist()
    description_list = [i.split() for i in description_list]
    alt_description_list = []
    for ingredients in description_list:
        sorted_ingredients = sorted(ingredients)
        new_string = " ".join(sorted_ingredients)
        alt_description_list.append(new_string)
    df_vegetable_products['sorted_name'] = alt_description_list
    df_sel_vegetable_products = df_vegetable_products[df_vegetable_products['sorted_name'].isin(ingredients_search)]
    df_grocery_list = pd.DataFrame()
    df_grocery_list['description'] = df_ingredients_table['sorted_name'][df_ingredients_table['food_category']=='vegetables']
    df_grocery_list['total_weight_in_lb'] = df_ingredients_table['recipe_weight_in_lb']/df_ingredients_table['recipe_yield']*df_ingredients_table['preferred_yield']
    df_grocery_list = df_grocery_list.merge(df_sel_vegetable_products, how='outer', on='description')
    df_grocery_list['cost'] = (df_grocery_list['lowest_price_per_lb'][df_grocery_list['soldBy']=='WEIGHT'])*(df_grocery_list['total_weight_in_lb'])
    df_grocery_list['cost'] = round(df_grocery_list['cost'].astype('float64'),2)
    df_grocery_list = df_grocery_list.dropna(subset=['productId'])
    df_grocery_list = df_grocery_list.drop(columns=IGNORE_GROCERY_COLS)
    df_grocery_list['total_costs'] = df_grocery_list['cost'].sum(axis=0)
    return df_grocery_list