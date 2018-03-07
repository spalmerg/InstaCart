import pandas as pd
import numpy as np
import random
from surprise import KNNBaseline
import pickle
import logging
import yaml


def build_recommender(data, model_meta):
    """ This function takes order, item, and rating data returns a
        KNN recommendation engine.

    Args:
        data: dataframe with columns order_id, product_id, and rating
        model_meta: original model_meta dict
        """

    from surprise import Dataset, Reader  # import libraries for EB
    logging.info('Setting up random state')
    random.seed(model_meta['train_recommender']['random_state'])

    np.random.seed(model_meta['train_recommender']['random_state'])
    logging.info('Setting up Surprise data reader')
    reader = Reader(rating_scale=(max(data.rating), min(data.rating)))

    logging.info('Calling load_from_df')
    data = Dataset.load_from_df(data, reader)  # reads and sets up data

    logging.info('Setting up recommender')
    k = model_meta['train_recommender']['neighbors']
    sim_options = model_meta['train_recommender']['sim_options']
    knn = KNNBaseline(k, sim_options=sim_options)  # collaborative filtering

    logging.info('Calling build_full_trainset')
    data = data.build_full_trainset()  # uses whole dataset to build model

    logging.info('Fit recommender')
    fit = knn.fit(data)  # fits model to data

    logging.info('Return recommender')
    return(fit)


def give_recommendation(model, raw_id, key):
    """This function takes a KNN model and a raw_id as input and returns the
    five nearest neighbors to the original item if the item was in the training
    set or the five most popular items if the original item was not in the
    training set.

    Args:
        model: trained KNN model from surprise package
        raw_id (str): the raw_id (InstCart ID) for the item
        key (dict): the product_id:product_name key dictionary

    Returns:
        Five recommendation items, five closest neighbors if known item or five
        most popular items if unknown item.
        """

    neighbors = {}  # initialize dictionary to hold recommendations
    try:
        inner_id = model.trainset.to_inner_iid(int(raw_id))  # insta->surprise
        inner_rec = model.get_neighbors(inner_id, 5)  # find neighbors
        # get instacart ids for each Surpise id
        raw_recs = [model.trainset.to_raw_iid(inner_id) for inner_id
                    in inner_rec]
        for rid in raw_recs:  # make instacart:item_name pairs
            neighbors[str(rid)] = key[str(rid)]
        return(neighbors)
    except:  # if bad item selectd, turn into popular recommendation engine
        return("RECOMMEND POPULAR ITEMS")


if __name__ == "__main__":
    log_fmt = '%(asctime)s -  %(levelname)s - %(message)s'
    logging.basicConfig(filename='setup.log', level=logging.INFO,
                        format=log_fmt)
    logger = logging.getLogger(__name__)

    logging.info('Reading in surprise csv')
    recommend = pd.read_csv("data/surprise.csv")

    logging.info('Reading in yaml file')
    with open('model_meta.yaml', 'r') as f:
        model_meta = yaml.load(f)

    logging.info('Building recommendation engine')
    fit = build_recommender(recommend, model_meta)

    logging.info('Pickling recommendation engine')
    pickle.dump(fit, open('models/model.pkl', 'wb'))
    logging.info('Pickling complete')
