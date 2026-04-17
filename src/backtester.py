import pandas as pd
import numpy as np


def vol_backtest(prices, rf_rates, target_vol=0.15, lookback=20, max_leverage=2.0, cost_per_trade=0.0005):
    base_returns = np.log(prices / prices.shift(1))
    realised_vol = base_returns.rolling(window=lookback).std() * np.sqrt(252)
    weights = target_vol / realised_vol
    valid_weights = weights.clip(upper=max_leverage)
    weight_used = valid_weights.shift(1)

    weight_change = weight_used.diff().abs()
    trading_costs = weight_change * cost_per_trade
    vol_returns = base_returns * weight_used + (1 - weight_used) * rf_rates - trading_costs
    total_vol_returns = vol_returns.cumsum().apply(np.exp)
    shifted_base_returns = base_returns.iloc[lookback + 1:]
    total_base_returns = shifted_base_returns.cumsum().apply(np.exp)

    results = pd.DataFrame({
        "base_returns": base_returns,
        "total_base_returns": total_base_returns,
        "weights": weight_used,
        "vol_returns": vol_returns,
        "total_vol_returns": total_vol_returns
    }).dropna()

    return results


def get_metrics(daily_returns, total_returns, risk_free_rate=0.04):
    annual_returns = np.exp(daily_returns.mean() * 252) - 1
    annual_volatility = daily_returns.std() * np.sqrt(252)
    sharpe_ratio = (annual_returns - risk_free_rate) / annual_volatility
    peak_returns = total_returns.cummax()
    drawdowns = (total_returns - peak_returns) / peak_returns
    max_drawdown = drawdowns.min()

    metrics = {
        "Annual returns": f"{annual_returns:.2%}",
        "Annual volatility": f"{annual_volatility:.2%}",
        "Sharpe ratio": f"{sharpe_ratio:.2f}",
        "Max_drawdown": f"{max_drawdown:.2%}"
    }

    return metrics
