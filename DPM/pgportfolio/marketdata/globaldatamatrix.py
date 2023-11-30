from __future__ import division
from __future__ import absolute_import
from __future__ import print_function


import numpy as np
import pandas as pd
from pgportfolio.tools.data import panel_fillna
from pgportfolio.constants import *
import sqlite3
from datetime import datetime
import logging



def get_global_panel_stock(start, end, period=300, features=('close',), stocks='stock_increase'):
    """
    :param start/end: linux timestamp in seconds
    :param period: time interval of each data access point
    :param features: tuple or list of the feature names
    :return a panel, [feature, coin, time]
    """
    if stocks == 'stock_increase':
        stock = np.load('pgportfolio/data/stock_increase.npy', allow_pickle=True)
    elif stocks == 'stock_no_change':
        stock = np.load('pgportfolio/data/stock_no_change.npy', allow_pickle=True)
    elif stocks == 'stock_decrease':
        stock = np.load('pgportfolio/data/stock_decrease.npy', allow_pickle=True)
    else:
        raise Exception('the given stocks is not there !!')

    coins = ['GOOG', 'NVDA', 'AMZN', 'AMD', 'QCOM', 'INTC', 'MSFT', 'AAPL', 'BIDU']

    logging.info("feature type list is %s" % str(features))

    stock_cols = ['date', 'high', 'low', 'open', 'close', 'volume', 'quoteVolume']

    print(stock.shape)

    time_index = pd.to_datetime(stock[0, :, 0])
    print(time_index)
    panel = pd.Panel(items=features, major_axis=coins, minor_axis=time_index, dtype=np.float32)


    for row_number, coin in enumerate(coins):
        chart = stock[row_number, :, :]
        df = pd.DataFrame(chart, columns=['date', 'high', 'low', 'open', 'close', 'volume', 'quoteVolume'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        for feature in features:
            panel.loc[feature, coin, :] = df.loc[:,feature].tolist()
            panel = panel_fillna(panel, "both")

    return panel

def get_global_panel_btc(start, end, period=300, features=('close',), stocks="stock_increase"):
    if stocks == 'btc_increase':
        panel = pd.read_pickle('pgportfolio/data/btc.pkl')
    elif stocks == 'btc_increase':
        panel = pd.read_pickle('pgportfolio/data/crix_2.pkl')
    elif stocks == 'btc_increase':
        panel = pd.read_pickle('pgportfolio/data/crix_3.pkl')
    elif stocks == 'btc_increase':
        panel = pd.read_pickle('pgportfolio/data/crix_4.pkl')
    else:
        print("no file")
    print(panel.shape)
    return panel
