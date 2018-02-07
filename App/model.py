import sqlite3
import pandas as pd
import numpy as np
from surprise import KNNBasic, Dataset, Reader

'''takes order_id, aisle_id, and rating and 
returns recommender from package surprise'''
def build_recommender(data):
  reader = Reader(rating_scale = (1,10))
  data = Dataset.load_from_df(data, reader)
  sim_options = {'name': 'cosine', 'user_based': False}
  knn = KNNBasic(sim_options = sim_options)
  data = data.build_full_trainset()
  return(knn.fit(data))

'''takes item_id and returns aisle_id'''
def item_to_aisle(item, products):
  a_id = products[products.product_id == item].aisle_id
  return(a_id.values[0])

'''takes an item, translates it to an aisle, finds nearest aisle neighbor
returns the most popular item in the neighboring aisle'''
def make_rec(item, knn, pop_dict, products):
    aisle = item_to_aisle(item, products)
    neighbor = knn.get_neighbors(aisle, k = 1)[0]
    item = pop_dict['product_name'][neighbor]
    return(item)





if __name__ == "__main__":
  #connect to database
  conn = sqlite3.connect("../instacart.db")

  #read in dataframes from database
  rec_data = pd.read_sql_query("SELECT * FROM rec_data", conn)
  pop_items = pd.read_sql_query("SELECT * FROM pop_items", conn)
  products = pd.read_sql_query("SELECT product_id, aisle_id FROM products", conn)

  #pop_items --> dictionary
  pop_dict = pop_items.to_dict()
  #print(pop_dict['product_name'][131])

  item = input("What do you want to buy? ")
  item = int(item)
  rec = build_recommender(rec_data)

  print(make_rec(item, rec, pop_dict, products))








