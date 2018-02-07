import sqlite3
import pandas as pd

def format_surprise(orders, products, aisles):
  data = pd.merge(orders, products, on = "product_id")
  data = data[["order_id", "aisle_id", "add_to_cart_order"]]
  data = pd.merge(data, aisles, on = "aisle_id")

  #find number items per order
  maxdf = pd.DataFrame(data.groupby(["order_id"])["add_to_cart_order"].agg("max"))
  maxdf = maxdf.reset_index()

  data = pd.merge(data, maxdf, on = "order_id")

  # get "rating " score based on when item was added to cart
  data["rating"] = (1 - data.add_to_cart_order_x / data.add_to_cart_order_y)*10
  data = data[["order_id", "aisle_id", "rating"]] #columns surprise needs

  return(data)

def top_items(orders, products):
  df = pd.merge(orders, products, on = "product_id")[['order_id', 'product_id', 'aisle_id', 'product_name']]
  df = df.groupby(['aisle_id', 'product_id']).agg('count')['order_id']
  df = df.reset_index()
  df = df.sort_values(['aisle_id', 'order_id'], ascending = False).groupby("aisle_id").first()
  df = pd.merge(df, products, on = "product_id")[['aisle_id', 'product_name']]
  return(df)


if __name__ == "__main__":
  #connect to database
  conn = sqlite3.connect("instacart.db")

  #read in dataframes from database
  aisles = pd.read_sql_query("SELECT * FROM aisles", conn)
  orders = pd.read_sql_query("SELECT * FROM orders", conn)
  products = pd.read_sql_query("SELECT * FROM products", conn)

  #format data
  rec_data = format_surprise(orders, products, aisles)
  pop_items = top_items(orders, products)

  rec_data.to_sql("rec_data", conn, if_exists ='replace', index=False)
  pop_items.to_sql("pop_items", conn, if_exists='replace', index=False)
