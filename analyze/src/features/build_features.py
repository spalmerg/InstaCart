import pandas as pd
import numpy as np
import logging
import yaml


def format_recommend(orders, count):
    """ This function takes the InstaCart orders dataframe and returns formats
    the dataframe for the surprise recommendation library of the top `count`
    products sold by InstaCart for model and app simplicity.

    Args:
        orders: Instacart order_products__train.csv
        count (int): the number of items to include in the recommendation
            engine

  Returns:
    Dataframe with columns order_id, product_id, and rating
    """
    logger = logging.getLogger(__name__)
    logger.info('Finding most popular products')

    counts = orders['product_id'].value_counts().reset_index().head(count)
    counts.columns = ['product_id', 'frequency_count']

    logger.info('Subsetting orders dataframe')
    orders = orders[orders.product_id.isin(counts.product_id)]

    logger.info('Transforming add_to_cart_order to rating')
    orders['rating'] = np.log(orders.add_to_cart_order)
    orders = orders[['order_id', 'product_id', 'rating']]

    logging.info('Returning dataframe')
    return(orders)


if __name__ == "__main__":
    log_fmt = '%(asctime)s -  %(levelname)s - %(message)s'
    logging.basicConfig(filename='setup.log', level=logging.INFO,
                        format=log_fmt)
    logger = logging.getLogger(__name__)

    logger.info("Reading in orders dataframe")
    orders = pd.read_csv("data/order_products__train.csv")

    logger.info("Reading in yaml file")
    with open('model_meta.yaml', 'r') as f:
        model_meta = yaml.load(f)

    logger.info("Calling format_recommend: building Surprise dataset")
    df = format_recommend(orders, model_meta['build_features']['item_count'])

    logger.info("Outputting Surprise dataset to CSV")
    df.to_csv("data/surprise.csv", index=False)

    logger.info("Data export complete")
