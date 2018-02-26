import pandas as pd
from sqlalchemy import create_engine, MetaData, Integer, Float, Table, Column, String
import config
import os
import psycopg2
import io
import logging

def db_define(env):
  """ This class defines the database schema 
  
  Args:
    env: database connection object

  """
  logger.info('sqlalchemy create_engine')
  engine = create_engine(env)
  meta = MetaData(bind=engine)

  logger.info('Define table')
  recommend = Table('recommend', meta,
    Column('order_id', Integer, primary_key=True, autoincrement=False),
    Column('product_id', Integer, primary_key=True, autoincrement=False),
    Column('rating', Float, nullable=True),
  )

  logger.info('Call create_all()')
  meta.create_all()


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

#read in surprise.csv 
  logger.info('Read in surprise csv')
  recommend = pd.read_csv("analyze/data/surprise.csv")

#set up buffer
  logger.info('Set up StringIO')
  buf_rec = io.StringIO()

#transfer to CSV format
  logger.info('Tranfer recommend table to csv through buf_rec')
  recommend.to_csv(buf_rec, header=False, index=False, sep='\t')

#reset the head
  logger.info('Reset CSV head')
  buf_rec.seek(0)

#write to database
  logger.info('Call copy_from')
  cur.copy_from(buf_rec, 'recommend', columns=('order_id', 'product_id', 'rating'))

  logger.info('Commit to database')
  connection.commit()

  logger.info('Close database connection')
  connection.close()

  logger.info('Database load complete')
