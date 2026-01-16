import pandas as pd


def load_macro_regimes() -> pd.DataFrame:
    data = [
        ("1971-01-01", "1981-01-01", "High Inflation Era"),
        ("1981-01-01", "2000-01-01", "Disinflation & Growth"),
        ("2000-01-01", "2008-01-01", "Dot-com & Credit Boom"),
        ("2008-01-01", "2009-06-01", "Global Financial Crisis"),
        ("2009-06-01", "2019-12-01", "QE / Low Rate Era"),
        ("2020-01-01", "2021-12-01", "COVID Shock"),
        ("2022-01-01", "2099-12-31", "Inflation & Tightening"),
    ]

    df = pd.DataFrame(data, columns=["start", "end", "macro_regime"])
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])
    return df


def tag_macro_regimes(df: pd.DataFrame, macro_df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["macro_regime"] = None

    for _, row in macro_df.iterrows():
        mask = (df.index >= row["start"]) & (df.index <= row["end"])
        df.loc[mask, "macro_regime"] = row["macro_regime"]

    return df
