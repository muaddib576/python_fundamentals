"""Evaluates product matching based on extracted feateres from provided data set"""

import pandas as pd
import numpy as np
from pprint import pprint
import re


def csv_read():
    """reads initial data from csv"""
    df1 = pd.read_csv("/users/brian/code_projects/1-extracted_data_final.csv", index_col = 0)
    
    # print(df1['brand_name'].isna().sum())
    # df1['brand_name'] = df1['brand_name'].fillna(df1['product_slug'])
    # print(df1['brand_name'].isna().sum())

    return df1

def brand_check(data):
    """If product_brand is null in initial data, checks to see if a known brand exists in product_slug or producte_description"""
    
    #creates reference list of known brands (this list is not the cleanest)
    raw_brands = data['brand_name'].dropna().unique()
    #convert to list cause i am bad at this
    # raw_brands = raw_brands.tolist()
    # raw_brands = list(set(raw_brands))
    # known_brands = []
    #use to convert brand values with '|'
    # double_brands = []
    '''
    for brand in unique_brands[0]:
        if '|' not in brand:
            known_brands.append(brand)
        else:
            double_brands.append(brand)
    print(double_brands)
    '''
    #manual list of pairs based on google search 1st = subbrand/product_name/other, 2nd = proper brand
    #Pride Wellness & Free Cannabis Co. are both real brands, but I am almost certain none of their products are in this data
    mapped_brands = {'green hornet':'cheeba chews',
                            'sublime': 'kanha',
                            'pride wellness': np.nan,
                            'chill': 'kiva',
                            'free cannabis': 'kushy punch',
                            'cresco': "mindy's",
                            "mindy's artisanal edibles": "mindy's",
                            'dose': 'glowing buddha',
                            'smokiez edibles': 'smokiez'
                        }
    print(raw_brands)
    print('--------------------')

    known_brands = []
    #removes known non-brands and adds the correct brand

    def brand_mapper(brand):
        for mbrand in mapped_brands:
            if str(mbrand) in str(brand):
                return mapped_brands[mbrand]
        return brand

    data['brand_name'] = data['brand_name'].apply(lambda x: brand_mapper(x))
    
    # for mbrand in mapped_brands:
    #     data['brand_name'] = data['brand_name'].replace(to_replace = mbrand,
    #                                                     value = mapped_brands[mbrand])


    raw_brands2 = data['brand_name'].dropna().unique()


    print(raw_brands2)
    print('fuckfuckfuck')

    known_brands = list(set(known_brands))            

    print(len(known_brands))
    print(known_brands)
    print('--------------------')

    double_brand_keys = {}
    for dbrand in double_brands:
        for kbrand in known_brands:
            if kbrand in dbrand:
                print(f"{dbrand} ------- {kbrand} \n")

    known_brands = np.asarray(known_brands)
    known_brands = np.reshape(known_brands, len(known_brands))
    print(known_brands)

    #create new slug and desc colums without hyphens and spaces to make matching easier
    data['slug_no_hyphen'] = data['product_slug'].str.replace('-','')
    data['desc_no_space'] = data['product_description'].str.replace(' ', '')


    
    # print(data['product_slug'])
    print(data)


    #
    for brand in known_brands:

        data.loc[data['slug_no_hyphen'].str.contains(brand, na=False) == True, 'backup_brand'] = brand
        
        # print(brand)
        # data[brand] = data['product_slug'].str.contains(brand)
        # print(data[brand].sum())
        data['backup_brand'].fillna(data['product_description'].str.contains(brand))
        # print(data[brand].sum())
    print(data[data['brand_name'].isnull()])
    
    df2 = data[data['brand_name'].isnull()]
    print(df2[df2['backup_brand'].isnull()])

    # print(df2[df2['product_slug'].str.contains('smokiez', na=False)])

    # data.loc[data['brand_name'] == 'NaN', data['backup_brand'] == 'NaN']
    # print(data)

    # print(known_brands)
    # print(data['product_slug'])
    # print(data)
    # print(data.loc[data['brand_name'] == 'om'])
    # print(data)
        
        
        # print("dis da brand compang------------:",brand)
        # print(data['product_slug'].str.contains(brand))

        # np.where(data['product_slug'].str.contains(brand) == True, )



    # for index, row in data.iterrows():
    #     if pd.isna(data['brand_name'][index]) == True:
    #         for brand in known_brands:
    #             if data['product_slug'][index].str.contains(brand) == True:
    #                 print(brand)

    
    return data

def main():

    raw_data = csv_read()
    # print(raw_data['brand_name'])
    raw_data = brand_check(raw_data)
    # print(raw_data['brand_name'])


main()
# csv_read()