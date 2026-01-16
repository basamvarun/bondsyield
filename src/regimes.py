import pandas as pd


def classify_yield_curve_regime(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    def classify(spread):
        if spread > 0.75:
            return "Normal Growth"
        elif spread > 0:
            return "Flattening"
        elif spread < 0:
            return "Inverted (Recession Risk)"
        return "Uncertain"

    df["regime"] = df["spread_1y_10y"].apply(classify)
    return df
