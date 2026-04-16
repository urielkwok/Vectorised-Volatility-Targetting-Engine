import pandas as pd
import numpy as np


def vol_engine(prices, target_vol=0.15, lookback=20, max_leverage=2.0):
    log_returns = np.log(prices / prices.shift(1))