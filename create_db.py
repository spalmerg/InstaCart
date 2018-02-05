from App import db
import pandas as pd
import sqlite3
from sqlalchemy import create_engine



def csv_to_db(name, filepath, con):
  df = pd.read_csv(filepath)
  df.to_sql(name, con, if_exists ='replace', index=False)


def 


if __name__ == "__main__":
  con = sqlite3.connect("instacart.db")
  cur = con.cursor()

  csv_to_db("orders","../instacart_2017_05_01/order_products__train.csv", con)
  csv_to_db("products", "../instacart_2017_05_01/products.csv", con)
  csv_to_db("aisles", "../instacart_2017_05_01/aisles.csv", con)