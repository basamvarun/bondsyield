import sys
import os

# --- Path Injection ---
# Add the project root to sys.path to ensure 'src' is discoverable on deployment
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Local Imports from the root-relative context
from src.data_loader import YieldDataLoader
from src.data_processor import clean_yield_data, merge_yield_curves
from src.indicators import calculate_spreads
from src.macro import load_macro_regimes, tag_macro_regimes
from src.regimes import classify_yield_curve_regime
from src.analytics import summarize_market_state

# --- Config ---
st.set_page_config(
    page_title="Yield Curve Research Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Caching Layers ---
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_processed_data(start_date, end_date):
    loader = YieldDataLoader()
    try:
        raw = {
            "1Y": clean_yield_data(loader.fetch_yield_data("1Y", str(start_date), str(end_date))),
            "5Y": clean_yield_data(loader.fetch_yield_data("5Y", str(start_date), str(end_date))),
            "10Y": clean_yield_data(loader.fetch_yield_data("10Y", str(start_date), str(end_date))),
        }
        
        df = merge_yield_curves(raw)
        df = calculate_spreads(df)
        
        macro = load_macro_regimes()
        df = tag_macro_regimes(df, macro)
        df = classify_yield_curve_regime(df)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# --- Sidebar ---
st.sidebar.header("📊 Research Parameters")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2015-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

st.sidebar.markdown("---")
st.sidebar.info(
    "This dashboard monitors US Treasury yields and classifies economic regimes based on curve spreads."
)

# --- Main App ---
st.title("📈 Yield Curve & Macro Research Dashboard")
st.markdown("Automated analysis of Treasury yields and macro-economic state.")

df = get_processed_data(start_date, end_date)

if df is not None:
    # Summary Section
    st.subheader("🧠 Research Summary")
    summary_col, info_col = st.columns([2, 1])
    
    with summary_col:
        st.success(summarize_market_state(df))
    
    with info_col:
        latest_spread = df['spread_1y_10y'].iloc[-1]
        delta = latest_spread - df['spread_1y_10y'].iloc[-2]
        st.metric("10Y-1Y Spread", f"{latest_spread:.2f}%", f"{delta:.2f}%")

    # Visuals
    tab1, tab2 = st.tabs(["Yield Curves", "Regime History"])
    
    with tab1:
        st.subheader("📊 Treasury Yields")
        fig = go.Figure()
        for t in ["1Y", "5Y", "10Y"]:
            fig.add_trace(go.Scatter(x=df.index, y=df[t], name=t, mode='lines'))
        fig.update_layout(
            hovermode="x unified", 
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📉 Yield Curve Spread (10Y – 1Y)")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df.index, y=df["spread_1y_10y"], name="10Y-1Y Spread", fill='tozeroy'))
        fig2.add_hline(y=0, line_dash="dash", line_color="red")
        fig2.update_layout(
            hovermode="x unified",
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("🌍 Historical Regimes")
        st.dataframe(df[["regime", "macro_regime", "1Y", "10Y", "spread_1y_10y"]].tail(50), use_container_width=True)
else:
    st.warning("Please adjust your date range or check your internet connection.")
