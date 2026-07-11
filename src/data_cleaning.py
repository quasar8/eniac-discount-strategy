import pandas as pd

url = 'your_products_csv_file_url_link'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
products = pd.read_csv(path)

url = 'your_brands_csv_file_url_link'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
brands = pd.read_csv(path)


url = 'your_orders_csv_file_url_link'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
orders = pd.read_csv(path)


url = 'your_orderlines_csv_file_url_link'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
orderlines = pd.read_csv(path)

orders_df = orders.copy()
products_df = products.copy()
brands_df = brands.copy()
orderlines_df = orderlines.copy()

# dropping 5 missing values in orders_df

orders_df = orders_df.dropna(axis=0)

# converting 'created_date' column into datetime type in orders_df
# converting 'date' in orderlines table to datetime

orders_df['created_date'] = pd.to_datetime(orders_df['created_date'])

orderlines_df['date'] = pd.to_datetime(orderlines_df['date'])

# figure out what percentage of data we will lose if we drop the rows that have 2 decimal points in the 'unit_price' column of orderlines_df

multi = (orderlines_df['unit_price'].str.count(r"\.")>1).sum()  #36.169 rows
total_rows = orderlines_df['unit_price'].count()
percantage = (multi*100/total_rows)
print (f'{percantage} % of data will be lost') # 12.3% of data will be lost

# if we delete these rows, we should also delete the other products belonging to the same id_order, otherwise the other tables won't be analysed correctly, so more rows will actually be lost
# check how many rows will actually be lost in total

lost_id_order = orderlines_df.loc[orderlines_df['unit_price'].str.count(r"\.")>1,'id_order']
how_many = orderlines_df.loc[orderlines_df['id_order'].isin(lost_id_order)].shape[0] # 77.733 rows will be deleted
real_percantage = (how_many*100 /total_rows)
print (f'{real_percantage} % of data actually will be lost')   #26.4% data, we will have 216250 remaining rows.

# let's convert unit_price to float, so 26.4% of data will disappear (because of the 2 decimal points problem)

orderlines_df = orderlines_df.loc[~orderlines_df['id_order'].isin(lost_id_order)]
orderlines_df["unit_price"] = pd.to_numeric(orderlines_df["unit_price"])


# there are 8746 duplicates in the products table, so remove them

products_df = products_df.drop_duplicates()

# but that was a general drop_duplicates(); we should also check the "sku" column specifically, since it should be unique
# to see both duplicate rows, keep=False should be used

products_df.loc[products_df['sku'].duplicated(keep=False)] # the second one has no price (NaN), so drop it
products_df.drop_duplicates(subset='sku', keep='first', inplace=True )


# missing values in the products table
# 7 missing values in the description column, just copy the product name into the description

products_df.loc[products_df['desc'].isna(),'desc'] = products_df.loc[products_df['desc'].isna(),'name']

# missing values in the price column

products_df['price'].isna().sum() # 45 values are missing, so missing values are 0.43%, we can drop them and price is very important info
products_df = products_df.dropna(subset=['price'])

# missing values in the type column, it is not necessary to drop them, keep them


# before converting price and promo_price to float, the 2 and 3 decimal points price problem should be solved
# how many prices have 2 decimal points?
## 2 decimal points    >>>   products_df.loc[products_df['price'].str.contains(r"\d+\.\d+\.\d+"),:]
## 3 digits after 1 decimal point >>>  products_df.loc[(products_df['price'].str.contains(r"\d+\.\d{3,}")), :]

price_problems_number = products_df.loc[(products_df.price.str.contains(r"\d+\.\d+\.\d+"))|(products_df.price.str.contains(r"\d+\.\d{3,}")), :].shape[0]   #542 problems

print(f"The column price has in total {price_problems_number} wrong values. This is {round(((price_problems_number / products_df.shape[0]) * 100), 2)}% of the rows of the DataFrame")

# this is 5.15% of the rows of the DataFrame, so we can delete them

products_df = products_df.loc[~((products_df['price'].str.contains(r"\d+\.\d+\.\d+"))|(products_df['price'].str.contains(r"\d+\.\d{3,}"))), :]
products_df["price"] = pd.to_numeric(products_df["price"])   # converting to float


# the promo_price column has many values with 2 decimal points or 3 digits after the decimal point

promo_problems_number = products_df.loc[(products_df.promo_price.str.contains(r"\d+\.\d+\.\d+"))|(products_df.promo_price.str.contains(r"\d+\.\d{3,}")), :].shape[0]
print(f"The column promo_price has in total {promo_problems_number} wrong values. This is {round(((promo_problems_number / products_df.shape[0]) * 100), 2)}% of the rows of the DataFrame")

#The column promo_price has in total 9232 wrong values. This is 92.39% of the rows of the DataFrame


products_cl = products_df.drop(columns=["promo_price"])


# new copy of those three dataframes

orders_qu = orders_df.copy()
orderlines_qu = orderlines_df.copy()
products_qu = products_cl.copy()

# keep only completed orders from orders_qu

orders_qu = orders_qu.loc[orders_qu['state']=='Completed', :]

# join orders_qu and orderlines_qu on order_id and id_order with an inner join, to keep only the common values

orders_orderlines = orders_qu.merge(orderlines_qu, how='inner', left_on='order_id', right_on='id_order')

# using the order_id values from this new DataFrame, keep only the matching ids in orders_qu and orderlines_qu

orders_qu = orders_qu.loc[orders_qu['order_id'].isin(orders_orderlines['order_id'].unique()), :]
orderlines_qu = orderlines_qu.loc[orderlines_qu['id_order'].isin(orders_orderlines['order_id'].unique())]

# exclude orders with unknown products: merge products_cl and orderlines_qu with a left join, left table is orderlines_qu

orderlines_products = orderlines_qu.merge(products_cl, how="left", on = "sku")[["id_order","sku","name" ]]

# masking the products whose name is NaN (unknown product)
orders_to_delete = orderlines_products.loc[orderlines_products['name'].isna(), "id_order"].unique()

# removing those order_id / id_order values from the orders_qu and orderlines_qu tables
orders_qu = orders_qu.loc[~orders_qu['order_id'].isin(orders_to_delete)]
orderlines_qu = orderlines_qu.loc[~orderlines_qu['id_order'].isin(orders_to_delete)]
