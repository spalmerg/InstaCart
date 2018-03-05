from sqlalchemy import create_engine, MetaData, Integer, Table, Column, Boolean
import os
import psycopg2
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
  Table('rec_orders', meta,
    Column('order_item_id', Integer, primary_key=True, autoincrement=True),
    Column('item_id', Integer, primary_key=False, autoincrement=False),
    Column('was_rec', Boolean, nullable=True),
    Column('rec_from', Integer, nullable=True)
  )

  logger.info('Call create_all()')
  meta.create_all()

def add_order(order):
  """ This function takes a dictionary of order items
  and adds the item id, whether or not it was a 
  recommended item, and if so, what item it was recommended
  for to the database

  Args:
    order (dict): nested dictionary with format 
    {item_id:{'was_rec':bool, 'rec_from':item_id}

  """
  # set up connection
  connection = psycopg2.connect(
  dbname = os.getenv("DATABASE"),
  user = os.getenv("USERNAME"),
  password = os.getenv("PASSWORD"),
  host = os.getenv("HOST")
  )
  cur = connection.cursor()
  #write each item in order to database
  for id in order.keys():
    cur.execute("INSERT INTO rec_orders (item_id, was_rec, rec_from) VALUES (%s,%s,%s)", \
      (id,order[id]['was_rec'],order[id]['rec_from']))
  # commit and close database connection 
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
