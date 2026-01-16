import pandas as pd


def summarize_market_state(df: pd.DataFrame) -> str:
    latest = df.iloc[-1]

    return (
        f"Regime: {latest['regime']} | "
        f"10Y–1Y Spread: {latest['spread_1y_10y']:.2f}% | "
        f"Macro Context: {latest['macro_regime']}"
    )
