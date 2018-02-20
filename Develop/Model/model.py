import psycopg2
import pandas as pd
import numpy as np
from surprise import KNNBaseline, Dataset, Reader
import os
import pickle

def get_data():
  """ This function connects to the database and returns a dataframe
  with order_id, product_id, and rating to be used in building the 
  recommendation engine. 

  """
  connection = psycopg2.connect(
    dbname = os.getenv("DATABASE"),
    user = os.getenv("USERNAME"),
    password = os.getenv("PASSWORD"),
    host = os.getenv("HOST"))
  cur = connection.cursor()
  cur.execute("SELECT * FROM recommend;")
  table = pd.DataFrame(cur.fetchall(), columns=['order_id', 'product_id', 'rating'])
  return(table)

def build_recommender(data):
  """ This function takes order, item, and rating data and exports a 
  pickled KNN recommendation engine. 

  Args: 
    data: dataframe with columns order_id, product_id, and rating

  """
  reader = Reader(rating_scale = (max(data.rating),0))
  data = Dataset.load_from_df(data, reader)
  knn = KNNBaseline(k=10, sim_options = {'name': 'pearson_baseline', 'user_based': False})
  data = data.build_full_trainset()
  fit = knn.fit(data)
  pickle.dump(fit, open('model.pkl', 'wb'))
  return(fit)

def give_recommendation(model, raw_id, key):
  """ This function takes a KNN model and a raw_id as input 
  and returns the five nearest neighbors to the original item 
  if the item was in the training set or the five most popular
  items if the original item was not in the training set. 
  
  Args: 
    model: trained KNN model from surprise package
    raw_id: the raw_id (InstCart ID) for the item
    key: the product_id/product_name key dictionary

  Returns: 
    Five recommendation items, five closest neighbors if known 
    item or five most popular items if unknown item. 

  """
  try:
    inner_id = model.trainset.to_inner_iid(int(raw_id))
    inner_rec = model.get_neighbors(inner_id, 5)
    raw_recs = [model.trainset.to_raw_iid(inner_id) for inner_id in inner_rec]
    neighbors = [key[str(rid)] for rid in raw_recs]
    return(neighbors)
  except: 
    return("RECOMMEND POPULAR ITEMS")

def get_products():
  """ This function connects to the database and returns a the 
  products dataframe to be used in the read_item_names function

  """
  connection = psycopg2.connect(
    dbname = os.getenv("DATABASE"),
    user = os.getenv("USERNAME"),
    password = os.getenv("PASSWORD"),
    host = os.getenv("HOST"))
  cur = connection.cursor()
  cur.execute("SELECT * FROM products;")
  table = pd.DataFrame(cur.fetchall(), columns=['product_id', 'product_name', 'aisle_id', 'department_id'])
  return(table)

def read_item_names(products,fit):
  """ This function reads the products table and exports 
  a pickled key of the product_id and product_name pairs

  Args: 
    products: the product dataframe read in from get_products()
    fit: a fitted KNN algorithm

  """
  rid_to_name = {}
  for i in range(0,len(products)):
    try:
      if fit.trainset.knows_item(fit.trainset.to_inner_iid(products.product_id[i])):
        rid_to_name[str(products.product_id[i])] = products.product_name[i]
    except:
      pass
  pickle.dump(rid_to_name, open('rid_to_name.pkl', 'wb'))



if __name__ == "__main__":
  fit = build_recommender(get_data())
  read_item_names(get_products(),fit)











