import pandas as pd
import numpy as np

def extract_strings_from_list(X):
    string = ''
    for i in range(len(X)):
        temp_string = X[i]
        if len(string) == 0:
            string = temp_string
        else:
            string = '; '.join([string, temp_string])
    return string

def json_list_to_dataframe(X):
    column_names = ['productId', 'categories','description']
    df = pd.DataFrame(X, columns = column_names)
    for column in column_names:
        temp_data = []
        for row in range(len(X)):
            temp_data.append(X[row][column])
        if column == 'categories':
            temp_data_2 = []
            for ind in range(len(temp_data)):
                tmp = temp_data[ind]
                temp_data_2.append(extract_strings_from_list(tmp))
            df[column] = temp_data_2
        else:
            df[column] = temp_data
    return df

def flatten_dict(X):
    X_dict = {}
    for key, value in X.items():
        if isinstance(value, dict):
            for k, v in value.items():
                new_key = key+'_'+k
                X_dict[new_key] = v
        else:
            X_dict[key] = value
    return X_dict

def json_product_items_to_dataframe(X):
    column_names = [
        'itemId', 'favorite', 'fulfillment_curbside', 'fulfillment_delivery', 'fulfillment_inStore', 
        'fulfillment_shipToHome', 'price_regular', 'price_promo', 'size', 'soldBy'
                   ]
    df = pd.DataFrame(X, columns = column_names)
    
    for column in column_names:
        temp_data = []
        for row in range(len(X)):
            data = flatten_dict(X[row]['items'][0])
            if column in data:
                temp_data.append(data[column])
            elif column not in data:
                temp_data.append('NaN')
            elif data[column] == 0: # no promo price
                temp_data.append('NaN')

        df[column] = temp_data
    return df

def combine_dataframes(df1, df2):
    final_df = pd.concat([df1, df2], axis=1)
    return final_df

def extract_product_info(X):
    X_products_id_categories_description = json_list_to_dataframe(X)
    X_vegetable_products_id_items = json_product_items_to_dataframe(X)
    X_vegetable_products_id_items['price_promo'] = X_vegetable_products_id_items['price_promo'].replace(0, np.nan)
    X_products = combine_dataframes(X_products_id_categories_description, X_vegetable_products_id_items)
    return X_products
