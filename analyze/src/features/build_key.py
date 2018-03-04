import psycopg2
import pandas as pd
import numpy as np
import os
import pickle
import logging

def read_item_names(products, fit):
  """ This function reads the products table returns a 
  dictionary formatted as key=product_id:value=product_name

  Args: 
    products: the product csv from Instacart
    """
  logger.info('Make empty dictionary')
  rid_to_name = {}
  logger.info('Begin looping through products')
  for i in range(0,len(products)):
    try:
      if fit.trainset.knows_item(fit.trainset.to_inner_iid(products.product_id[i])):
        rid_to_name[str(products.product_id[i])] = products.product_name[i]
    except:
      pass
  logger.info('Return key dictionary')
  return(rid_to_name)


if __name__ == "__main__":
  log_fmt = '%(asctime)s -  %(levelname)s - %(message)s'
  logging.basicConfig(filename='setup.log', level=logging.INFO, format=log_fmt)
  logger = logging.getLogger(__name__)
  
  logger.info('Reading in products dataframe')
  products = pd.read_csv("data/products.csv")

  logger.info('Unpickle model')
  model = pickle.load(open("models/model.pkl", "rb"))

  logger.info('Call read_item_names')
  key = read_item_names(products, model)

  logger.info('Pickle key')
  pickle.dump(key, open('models/rid_to_name.pkl', 'wb'))

  logger.info('Key export successful')