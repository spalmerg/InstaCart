import pandas as pd
import pickle
import yaml
import sys
sys.path.append("..")
from src.models import model as m


# read in yaml file for testing
with open('../model_meta.yaml', 'r') as f:
    model_meta = yaml.load(f)

# load in model and key to test
model = pickle.load(open("../models/model.pkl", "rb"))
key = pickle.load(open("../models/rid_to_name.pkl", "rb"))
data = pd.read_csv("../data/surprise.csv")


def test_bad_item():
    """make sure that a fake item returns popular items"""
    bad = m.give_recommendation(model, "meow", key)
    assert (bad == "RECOMMEND POPULAR ITEMS")


def test_good_item():
    """test that a real key returns five recommended items"""
    rec = m.give_recommendation(model, "47526", key)
    assert len(rec) == 5


def test_build():
    """test that the new recommender returns neighbors"""
    rec = m.build_recommender(data, model_meta)
    assert len(rec.get_neighbors(1, 5)) == 5


def test_rec():
    """check for same recommendation for random state 12"""
    rec = m.build_recommender(data, model_meta)
    assert rec.get_neighbors(1, 5) == [130, 115, 343, 18, 144]
