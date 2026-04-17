import pandas as pd
import src.data_loader as dl
import src.backtester as bt
import src.visualizer as vz

TICKER = "AMZN"

prices = dl.pull_data(TICKER)
results = bt.vol_backtest(prices[TICKER])
base_metrics = bt.get_metrics(results["base_returns"], results["total_base_returns"])
vol_metrics = bt.get_metrics(results["vol_returns"], results["total_vol_returns"])
metrics_df = pd.DataFrame({
    "Base": base_metrics,
    "Strategy": vol_metrics
})
print(metrics_df)
vz.create_plots(results)
