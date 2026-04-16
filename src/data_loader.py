import yfinance as yf


def pull_data(ticker, start="2024-1-1", end="2026-1-1"):
    df = yf.download(ticker, start, end)
    df = df["Close"].copy()
    df = df.dropna()
    return df
