import pandas as pd
import sys
sys.path.append("..")
from src.features import build_features as bf


data = pd.read_csv("../data/order_products__train.csv")


def test_format():
    """test that function returns correct # of items"""
    df = bf.format_recommend(data, 10)
    assert len(set(df.product_id)) == 10


def test_dimensions():
    """check that function returns correct # of columns"""
    df = bf.format_recommend(data, 10)
    assert df.shape[1] == 3


def test_colnames():
    """check that columns are named correctly for Surprise"""
    df = bf.format_recommend(data, 10)
    assert list(df) == ['order_id', 'product_id', 'rating']
