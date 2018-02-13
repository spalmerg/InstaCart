import psycopg2
import pandas as pd
import numpy as np
from surprise import KNNBasic, Dataset, Reader
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
  cur.execute("SELECT * FROM recommend LIMIT 10000;") # this should be as big as possible
  table = pd.DataFrame(cur.fetchall(), columns=['order_id', 'product_id', 'rating'])
  return(table)

def build_recommender(data):
  """ This function takes order, item, and rating data and exports a 
  pickled KNN recommendation engine. 

  Args: 
    param1: dataframe with columns order_id, product_id, and rating

  """
  reader = Reader(rating_scale = (max(data.rating),0))
  data = Dataset.load_from_df(data, reader)
  knn = KNNBasic(sim_options = {'name': 'cosine', 'user_based': False})
  data = data.build_full_trainset()
  pickle.dump(knn.fit(data), open('model.pkl', 'wb'))

def give_recommendation(model, raw_id):
  """ This function takes a KNN model and a raw_id as input 
  and returns the five nearest neighbors to the original item 
  if the item was in the training set or the five most popular
  items if the original item was not in the training set. 
  
  Args: 
    param1: trained KNN model from surprise package
    param2: the raw_id (InstCart ID) for the item

  Returns: 
    Five recommendation items, five closest neighbors if known 
    item or five most popular items if unknown item. 

  """
  try:
    inner_id = model.trainset.to_inner_iid(int(raw_id))
    inner_rec = model.get_neighbors(inner_id, 5)
    raw_recs = [model.trainset.to_raw_iid(inner_id) for inner_id in inner_rec]
    return(raw_recs)
  except: 
    return("RECOMMEND POPULAR ITEMS")



if __name__ == "__main__":
  build_recommender(get_data())











