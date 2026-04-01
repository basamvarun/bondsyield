""
import pandas as pd

def clean_yield_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna().drop_duplicates("date")
    return df.sort_values("date")


def merge_yield_curves(dfs: dict) -> pd.DataFrame:
    merged = None

    for tenor, df in dfs.items():
        if merged is None:
            merged = df
        else:
            merged = pd.merge(merged, df, on="date")
    return merged.sort_values("date")
  ""