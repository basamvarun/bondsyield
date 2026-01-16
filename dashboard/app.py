import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from src.data_loader import YieldDataLoader
from src.data_processor import clean_yield_data, merge_yield_curves
from src.indicators import calculate_spreads
from src.macro import load_macro_regimes, tag_macro_regimes
from src.regimes import classify_yield_curve_regime
from src.analytics import summarize_market_state

st.set_page_config(page_title="Yield Curve Research Dashboard", layout="wide")
st.title("📈 Yield Curve & Macro Research Dashboard")

# Sidebar
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2015-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Load data
loader = YieldDataLoader()
raw = {
    "1Y": clean_yield_data(
        loader.fetch_yield_data("1Y", str(start_date), str(end_date))
    ),
    "5Y": clean_yield_data(
        loader.fetch_yield_data("5Y", str(start_date), str(end_date))
    ),
    "10Y": clean_yield_data(
        loader.fetch_yield_data("10Y", str(start_date), str(end_date))
    ),
}

df = merge_yield_curves(raw)
df = calculate_spreads(df)

macro = load_macro_regimes()
df = tag_macro_regimes(df, macro)
df = classify_yield_curve_regime(df)

# Summary
st.subheader("🧠 Research Summary")
st.success(summarize_market_state(df))

# Yield Chart
st.subheader("📊 Treasury Yields")
fig = go.Figure()
for t in ["1Y", "5Y", "10Y"]:
    fig.add_trace(go.Scatter(x=df.index, y=df[t], name=t))
st.plotly_chart(fig, use_container_width=True)

# Spread Chart
st.subheader("📉 Yield Curve Spread (10Y – 1Y)")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df.index, y=df["spread_1y_10y"]))
fig2.add_hline(y=0, line_dash="dash", line_color="red")
st.plotly_chart(fig2, use_container_width=True)

# Regime Table
st.subheader("🌍 Latest Regimes")
st.dataframe(df[["regime", "macro_regime"]].tail(10))
