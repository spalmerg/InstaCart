from sqlalchemy import create_engine, MetaData, Integer, Table, Column, Boolean
import config
import os
import psycopg2
import io
import logging

def db_define(env):
  """ This function defines the database schema 
  
  Args:
    env: database connection object

  """
  logger.info('sqlalchemy create_engine')
  engine = create_engine(env)
  meta = MetaData(bind=engine)

  logger.info('Define table')
  rec_orders = Table('rec_orders', meta,
    Column('order_item_id', Integer, primary_key=True, autoincrement=True),
    Column('item_id', Integer, primary_key=False, autoincrement=False),
    Column('was_rec', Boolean, nullable=True),
  )

  logger.info('Call create_all()')
  meta.create_all()

def add_order(order):
  """ This function takes a dictionary of order items
  and adds the item id and whether or not it was a 
  recommended item to the database

  Args:
    order: a dictionary formatted item_id:bool which specifies the 
    ordered item and whether or not it was recommended

  """
  connection = psycopg2.connect(
  dbname = os.getenv("DATABASE"),
  user = os.getenv("USERNAME"),
  password = os.getenv("PASSWORD"),
  host = os.getenv("HOST")
  )
  cur = connection.cursor()
  for woof in order.keys():
    print(woof)
    cur.execute("INSERT INTO rec_orders (item_id, was_rec) VALUES (%s,%s)", (woof,order[woof]))
  connection.commit()
  connection.close()


if __name__ == "__main__":
  # set up logging
  log_fmt = '%(asctime)s -  %(levelname)s - %(message)s'
  logging.basicConfig(filename='create_db.log', level=logging.INFO, format=log_fmt)
  logger = logging.getLogger(__name__)

  #set up database and connection
  logger.info('Get database url from environment')
  db = db_define(os.environ.get("DATABASE_URL"))

  logger.info('Set up database connection')
  connection = psycopg2.connect(
    dbname = os.getenv("DATABASE"),
    user = os.getenv("USERNAME"),
    password = os.getenv("PASSWORD"),
    host = os.getenv("HOST")
    )
  cur = connection.cursor()
