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




# First issue encountered : some categories only has a few sellings (e.g only 3 recorded sales) and some others have thousands. 
# -> How to solve this? 1st tought: suppose that sales are 0

# The main challenge will be how to decide how to drop data?. !








# Data Standardization 
