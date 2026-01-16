import pandas as pd


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["signal"] = "Neutral"

    # Oversold Yield (mean reversion zone)
    df.loc[
        (df["rsi"] < 30) & (df["close"] <= df["bb_lower"]),
        "signal"
    ] = "Oversold Yield (Possible Mean Reversion)"

    # Overbought Yield (reversal risk)
    df.loc[
        (df["rsi"] > 70) & (df["close"] >= df["bb_upper"]),
        "signal"
    ] = "Overbought Yield (Reversal Risk)"

    # Volatility Regime
    df["bb_width"] = df["bb_upper"] - df["bb_lower"]
    vol_base = df["bb_width"].rolling(20).mean()
    df.loc[df["bb_width"] > vol_base, "signal"] = "High Volatility Regime"

    # Macro override (if present)
    if "macro_event" in df.columns:
        df.loc[df["macro_event"].notna(), "signal"] = "Macro Event – Elevated Rate Sensitivity"

    return df
