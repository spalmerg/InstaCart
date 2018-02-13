import pandas as pd
import numpy as np
from sqlalchemy import create_engine, MetaData, Integer, Float, Table, Column, String
import config
import os
import psycopg2
import io

def format_recommend(orders):
  """ This function takes the InstaCart orders dataframe 
  and returns formats the dataframe for the surprise 
  recommendation library.

  Args: 
    orders(csv): Instacart order_products__train.csv

  Returns:
    Dataframe with columns order_id, product_id, and rating

  """
  orders['ratings'] = np.log(orders.add_to_cart_order)
  orders = orders[['order_id', 'product_id','ratings']]
  return(orders)

def db_define(env):
  """ This class defines the database schema 
  
  Args:
    env: database connection object

  """
  engine = create_engine(env)#
  meta = MetaData(bind=engine)

  recommend = Table('recommend', meta,
    Column('order_id', Integer, primary_key=True, autoincrement=False),
    Column('product_id', Integer, primary_key=True, autoincrement=False),
    Column('rating', Float, nullable=True),
  )
  products = Table('products', meta,
    Column('product_id', Integer, primary_key=True, autoincrement=False),
    Column('product_name', String, primary_key=True, autoincrement=False),
    Column('aisle_id', Integer, primary_key=True, autoincrement=False),
    Column('department_id', Integer, nullable=True),
  )
  meta.create_all()


if __name__ == "__main__":
  #set up database and connection
  db = db_define(os.environ.get("DATABASE_URL"))
  connection = psycopg2.connect(
    dbname = os.getenv("DATABASE"),
    user = os.getenv("USERNAME"),
    password = os.getenv("PASSWORD"),
    host = os.getenv("HOST")
    )
  cur = connection.cursor()

#read in csvs
  orders = pd.read_csv("../Data/order_products__train.csv")
  products = pd.read_csv("../Data/products.csv")

#reformat recommend table
  recommend = format_recommend(orders)

#set up buffers
  buf_prod = io.StringIO()
  buf_rec = io.StringIO()

#transfer to CSV format
  products.to_csv(buf_prod, header=False, index=False, sep='\t')
  recommend.to_csv(buf_rec, header=False, index=False, sep='\t')

#reset the head
  buf_prod.seek(0)
  buf_rec.seek(0)

#write to database
  cur.copy_from(buf_prod, 'products', columns=('product_id','product_name','aisle_id','department_id'))
  cur.copy_from(buf_rec, 'recommend', columns=('order_id', 'product_id', 'rating'))
  connection.commit()
  connection.close()
