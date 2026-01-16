import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta


class YieldDataLoader:
    """
    Fetches market-determined US Treasury yields from Yahoo Finance.
    """

    TICKER_MAP = {
        "1Y": "^IRX",  # Short-term proxy
        "5Y": "^FVX",  # 5-Year Treasury
        "10Y": "^TNX",  # 10-Year Treasury
    }

    def __init__(self, data_dir="data/raw"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def fetch_yield_data(self, asset, start_date=None, end_date=None):

        if asset not in self.TICKER_MAP:
            raise ValueError(f"Asset must be one of {list(self.TICKER_MAP.keys())}")

        if end_date is None:
            end_date = datetime.now()
        elif isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        if start_date is None:
            start_date = end_date - timedelta(days=365 * 10)
        elif isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d")

        ticker = self.TICKER_MAP[asset]
        print(f"Fetching {asset} yield data...")

        df = yf.download(ticker, start=start_date, end=end_date, progress=False)
        if df.empty:
            raise ValueError("No data returned")

        df.reset_index(inplace=True)

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]

        df.columns = [c.lower().replace(" ", "_") for c in df.columns]

        df = df[["date", "close"]]
        df.rename(columns={"close": asset}, inplace=True)

        return df
