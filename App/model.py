import sqlite3
import pandas as pd
import numpy as np
from scipy.sparse import csc_matrix
from lightfm import LightFM

# function adds new order to matrix
def new_order(shopping_cart, df):
    temp = pd.DataFrame(0, index=np.arange(1), columns = np.arange(df.shape[1]))
    temp.columns = df.columns
    for i in shopping_cart:
        temp.ix[0,i] = 1
    return(df.append(temp))

# builds recommender with new order included
def train_model(df):
    df.sparse = csc_matrix(df)
    model = LightFM(loss='warp')
    model.fit(df.sparse, epochs = 10, num_threads = 1)
    return(model)

def get_recs(model, shopping_cart, df, aisles):
    other_products = np.array(df.columns.drop(shopping_cart))
    scores = model.predict(0, np.array(other_products))
    top_items = np.argsort(-scores)[0:3]
    
    for aid in top_items: 
        print(aisles[aisles.aisle_id == aid]["aisle"].values[0])




if __name__ == "__main__":
  #connect to database
  conn = sqlite3.connect("../instacart.db")

  #read in dataframes from database
  matrix = pd.read_sql_query("SELECT * FROM matrix", conn)
  aisles = pd.read_sql_query("SELECT * FROM aisles", conn)

  # new user example
  shopping_cart = ['1'] # user input
  ORDER = new_order(shopping_cart, matrix)

  # train model with new order data
  model = train_model(ORDER)

