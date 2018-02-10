import pandas as pd
from sqlalchemy import create_engine, MetaData, Integer, Float, Table, Column, String
from sqlalchemy import MetaData
import config
import os
import psycopg2
import io

def format_surprise(orders,products,aisles):
  data = pd.merge(orders, products, on = "product_id")
  data = pd.merge(data, aisles, on = "aisle_id")
  maxdf = pd.DataFrame(data.groupby(["order_id"])["add_to_cart_order"].agg("max"))
  maxdf = maxdf.reset_index()
  data = pd.merge(data, maxdf, on = "order_id")
  data["rating"]=(1-data.add_to_cart_order_x/data.add_to_cart_order_y)*10
  data = data[["order_id", "aisle_id", "rating"]].reset_index()
  return(data)

def top_items(orders,products):
  df = pd.merge(orders, products, on = "product_id")[['order_id', 'product_id', 'aisle_id', 'product_name']]
  df = df.groupby(['aisle_id', 'product_id']).agg('count')['order_id']
  df = df.reset_index()
  df = df.sort_values(['aisle_id', 'order_id'], ascending = False).groupby("aisle_id").first()
  df = pd.merge(df, products, on = "product_id")[['aisle_id', 'product_name']]
  return(df)

class db_define(object):
  engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
  meta = MetaData(bind=engine)

  surprise = Table('surprise', meta,
    Column('index', Float, primary_key=True, autoincrement=False),
    Column('order_id', Integer, primary_key=True, autoincrement=False),
    Column('aisle_id', Integer, primary_key=True, autoincrement=False),
    Column('rating', Float, nullable=True),
  )

  popitems = Table('popitems', meta,
    Column('aisle_id', Integer, primary_key=False, autoincrement=False),
    Column('product_name', String, nullable=True)
  )
  meta.create_all()


if __name__ == "__main__":
  #set up database and connection
  db = db_define()
  connection = psycopg2.connect(
    dbname = os.getenv("DATABASE"),
    user = os.getenv("USERNAME"),
    password = os.getenv("PASSWORD"),
    host = os.getenv("HOST")
    )
  cur = connection.cursor()

#read in csv
  orders = pd.read_csv("Data/order_products__train.csv")
  products = pd.read_csv("Data/products.csv")
  aisles = pd.read_csv("Data/aisles.csv")

#reformat data
  surprise = format_surprise(orders,products,aisles)
  popitems = top_items(orders,products)

  buf_pop = io.StringIO()
  buf_sup = io.StringIO()
  surprise = surprise.to_csv(buf_sup, header=False, index=False, sep='\t')
  popitems = popitems.to_csv(buf_pop, header=False, index=False, sep='\t')
  buf_pop.seek(0)
  buf_sup.seek(0)

#write to database
  cur.copy_from(buf_pop, 'popitems',columns=('aisle_id','product_name'))
  cur.copy_from(buf_sup, 'surprise',columns=('index','order_id','aisle_id','rating'))
  connection.commit()
  connection.close()
