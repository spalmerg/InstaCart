import pandas as pd
import pickle
import sys
sys.path.append("..")
from src.features import build_key as bk


model = pickle.load(open("../models/model.pkl", "rb"))
key = pickle.load(open("../models/rid_to_name.pkl", "rb"))
data = pd.read_csv("../data/products.csv")


def test_isdict():
    """check that function returns dictionary"""
    key = bk.read_item_names(data, model)
    assert isinstance(key, dict)


def test_keyval():
    """check that function returns correct key/pair"""
    key = bk.read_item_names(data, model)
    assert key['38739'] == 'Hass Avocado'


def test_bad():
    """test incorrect key returns nothing"""
    key = bk.read_item_names(data, model)
    assert key.get('not a key', 'empty')
