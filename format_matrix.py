import sqlite3
import pandas as pd

def relevel_aisle_id(df):
    df.aisle_id = df.aisle_id - 1
    return(df)

def build_matrix(orders, products, aisles):
    # make big dataframe
    ord_prod = pd.merge(orders, products, on = "product_id")
    data = pd.merge(ord_prod, aisles, on = "aisle_id")
    data = data[["order_id", "aisle", "aisle_id"]]
    
    # return matrix and de-level 
    df = data.pivot_table(index = ["order_id"], columns = ["aisle_id"], aggfunc = "count", fill_value = 0)
    return(df.aisle)


if __name__ == "__main__":
  #connect to database
  conn = sqlite3.connect("instacart.db")

  #read in dataframes from database
  aisles = pd.read_sql_query("SELECT * FROM aisles", conn)
  orders = pd.read_sql_query("SELECT * FROM orders", conn)
  products = pd.read_sql_query("SELECT * FROM products", conn)

  #relevel aisle IDs for recommender
  aisles = relevel_aisle_id(aisles)
  products = relevel_aisle_id(products)

  #build matrix
  data = build_matrix(orders, products, aisles)
  data.to_sql("matrix", conn, if_exists ='replace', index=False)
