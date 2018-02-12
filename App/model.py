import psycopg2
import pandas as pd
import numpy as np
from surprise import KNNBasic, Dataset, Reader
import os
import pickle

def get_data():
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
  reader = Reader(rating_scale = (4.5,0))
  data = Dataset.load_from_df(data, reader)
  knn = KNNBasic(sim_options = {'name': 'cosine', 'user_based': False})
  data = data.build_full_trainset()
  pickle.dump(knn.fit(data), open('model.pkl', 'wb'))


if __name__ == "__main__":
  build_recommender(get_data())











