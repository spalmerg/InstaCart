#from App import db
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Integer, Float, Table, Column, String
from sqlalchemy import MetaData
import config
import os
import psycopg2


class db_define(object):
  engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
  meta = MetaData(bind=engine)

  orders = Table('orders', meta,
    Column('order_id', Integer, primary_key=True, autoincrement=False),
    Column('product_id', Integer, nullable=True),
    Column('add_to_cart_order', Integer, nullable=True),
    Column('reordered', String, nullable=True)
  )

  products = Table('products', meta,
    Column('product_id', Integer, primary_key=True, autoincrement=False),
    Column('product_name', String, nullable=True),
    Column('aisle_id', Integer, nullable=True),
    Column('department_id', Integer, nullable=True)
    )
 
  aisle = Table('aisle', meta,
    Column('aisle_id', Integer, primary_key=True, autoincrement=False),
    Column('aisle', String, nullable=True),
    )


if __name__ == "__main__":
  db = db_define()
  db.meta.create_all(db.engine)

  con = create_engine(os.environ.get("DATABASE_URL"))

  orders = pd.read_csv("../instacart_2017_05_01/order_products__train.csv")
  products = pd.read_csv("../instacart_2017_05_01/products.csv")
  aisles = pd.read_csv("../instacart_2017_05_01/aisles.csv")

  orders.head().to_sql("orders", con, if_exists='replace', index=False)
  products.head().to_sql("products", con, if_exists='replace', index=False)
  aisles.head().to_sql("aisles", con, if_exists='replace', index=False)
