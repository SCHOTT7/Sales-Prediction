# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 18:41:35 2022

@author: Victo
"""
# Package required

import pandas as pd
import numpy as np
import plotly.express as px
import collections
from plotly.offline import plot
from datetime import datetime
import matplotlib.pyplot as plt

# Data importation

PATH = 'D:\\data\\Predict Future Sales\\'

items = pd.read_csv(PATH+'items.csv')
item_categories = pd.read_csv(PATH+'item_categories.csv')
shops = pd.read_csv(PATH+'shops.csv')
sales_train = pd.read_csv(PATH+'sales_train.csv')




# Data exploration

sales_train.columns
sales_train.head()


cat_frequence =collections.Counter(items['item_category_id'])
fig = px.bar(x=cat_frequence.keys(), y=cat_frequence.values())
fig.show()
plot(fig)

shop_frequence = collections.Counter(sales_train['shop_id'])
fig = px.bar(x = shop_frequence.keys(), y = shop_frequence.values())
fig.show()
plot(fig)


#Check seasonnality 
# Daily
sales_freq_day = collections.Counter(sales_train['date'])
fig = px.bar(x = sales_freq_day.keys(), y = sales_freq_day.values())
plot(fig)

# Monthly

sales_freq_month =collections.Counter(sales_train['date_block_num'])
fig = px.bar(x = sales_freq_month.keys(), y = sales_freq_month.values())
plot(fig)
# We observer a certain tendency in these data

# My first objective with this dataset in to integrate the month, the week, the week of the month, the day of the week,
# in a way to identify tendencies for each product/product category in each shop 


sales_train['month'] = [date[3:5] for date in sales_train['date']]
sales_train['day'] = [date[0:2] for date in sales_train['date']]
dates_dt = [datetime.strptime(date,"%d.%m.%Y") for date in sales_train['date']]
sales_train['weekday'] = [date.weekday() for date in dates_dt]
sales_train['year'] = [date[6:] for date in sales_train['date']]
sales_train['yearmonth'] = sales_train['year'] + '_'+ sales_train['month']


from math import ceil

def week_of_month(dt):
    """ Returns the week of the month for the specified date.
    """

    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))

sales_train['monthweek'] = [week_of_month(date) for date in dates_dt]

sales_train[:50][['date','day','monthweek']]


## Now I'll divide our global sales data set in several subset, one for each shop

# To achieve this, ill create a dict of dataframes
shops_sales = {}
keys =shops.iloc[:,1]
for shop_id in keys:
    shops_sales[shop_id] = sales_train[sales_train['shop_id'] == shop_id]


#Now, I have to catch different tendencies :
    # One tendency for each global sales of a category
    # One tendency for each product product of a category
    # One tendency for each shops
    # One tendency for each category in each shop
    # One tendency for each product in each shop
    
# And this, at different time intervals : 1. Monthly, then 2. MonthWeekly, then 3. WeekDaily


# Let's start with monthly, global, product categories tendency
sales_train['date_dt'] = dates_dt
sales_train = sales_train.sort_values(by=['date_dt'])

sales_train = pd.merge(sales_train, items, how = 'left')

prod_categories = {}
keys = item_categories.iloc[:,1]
for item_cat in keys:
    prod_categories[item_cat] = sales_train[sales_train['item_category_id'] == item_cat]


items_sales ={}
keys = items['item_id']
for item_id in keys:
    items_sales[item_id] = sales_train[sales_train['item_id'] == item_id]


prod_categories[23].columns
sales_23_month =collections.Counter(prod_categories[23]['yearmonth'])

print('Monthly sales of product 23')
plt.figure(100, figsize = (12,5))
plt.plot(sales_23_month.keys(), sales_23_month.values())

print('Weekly sales of product 23')
sales_23_week =collections.Counter(prod_categories[23]['yearmonth']+prod_categories[23]['weekday'].astype(str))
plt.figure(100, figsize = (12,5))
plt.plot(sales_23_week.keys(), sales_23_week.values())



# First issue encountered : some categories only has a few sellings (e.g only 3 recorded sales) and some others have thousands. 
# -> How to solve this? 1st tought: suppose that sales are 0

# The main challenge will be how to decide how to drop data?. !

# Lets try with an example, I'll consider one product globaly and try to work with it

# Count most sold items
sales_n = []
for item in items_sales.keys():
    sales_n.append(sum(items_sales[item]['item_cnt_day']))
    
sales_count = pd.DataFrame(data=sales_n, index = items_sales.keys())

sales_count = sales_count.sort_values(by = 0, ascending = False)
print(sales_count.head())

item2808_sales = items_sales[2808]
item2808_monthlysales = item2808_sales[['item_cnt_day','yearmonth']].groupby('yearmonth').sum()
plt.plot(item2808_monthlysales.index,item2808_monthlysales['item_cnt_day'])

     

def generate_time_lags(df, n_lags):
    df_n = df.copy()
    for n in range(1, n_lags + 1):
        df_n[f"lag{n}"] = df_n["item_cnt_day"].shift(n)
    df_n = df_n.iloc[n_lags:]
    return df_n
    
input_dim = 400

sales_item2808_generated = generate_time_lags(item2808_sales, input_dim)

# Let's separate values (sales) from features (dates / locations)

def onehot_encode_pd(df, col_name):
    dummies = pd.get_dummies(df[col_name], prefix=[col_name])
    return pd.concat([df, dummies], axis=1).drop(columns=[col_name])

sales_item2808_features = item2808_sales

def generate_cyclical_features(df, col_name, period, start_num=0):
    kwargs = {
        f'sin_{col_name}' : lambda x: np.sin(2*np.pi*(df[col_name].astype(int)-start_num)/period),
        f'cos_{col_name}' : lambda x: np.cos(2*np.pi*(df[col_name].astype(int)-start_num)/period)    
             }
    return df.assign(**kwargs).drop(columns=[col_name])


for col_name in ['month','day','weekday','monthweek','yearmonth']:
    sales_item2808_features = generate_cyclical_features(sales_item2808_features, col_name, sales_item2808_features[col_name].astype(int).max(), sales_item2808_features[col_name].astype(int).min())
    




for col_name in  list(sales_item2808_features.columns[10:]):
    dummies = pd.get_dummies(sales_item2808_features[col_name], prefix=col_name)
    sales_item2808_features = pd.concat([sales_item2808_features, dummies], axis = 1).drop(columns = col_name)
sales_item2808_features = sales_item2808_features.iloc[:, 10:]







# Data Standardization 
