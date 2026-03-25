import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="Commodity Scalper Pro")
st.title("🥈 Silver & 🛢️ Oil Scalping Analyzer")

# 2. Sidebar Settings
with st.sidebar:
    st.header("⚙️ Strategy Settings")
    symbol = st.selectbox("Asset", ["SI=F", "CL=F"], index=0)
    timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "30m", "1h"], index=1)
    bb_length = st.slider("Bollinger Length", 10, 50, 20)
    rsi_length = st.slider("RSI Length", 5, 30, 14)
    st.markdown("---")
    st.info("Strategy: Buy at Lower BB + RSI < 35 | Sell at Upper BB + RSI > 65")

# 3. Data Loading
@st.cache_data(ttl=30)
def get_data(ticker, interval):
    df = yf.download(ticker, period="2d", interval=interval)
    if df.empty: return pd.DataFrame()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.columns = [col.lower() for col in df.columns]
    return df

df = get_data(symbol, timeframe)

if not df.empty:
    # 4. Technical Analysis
    df['rsi'] = ta.rsi(df['close'], length=rsi_length)
    bbands = ta.bbands(df['close'], length=bb_length, std=2)
    df = pd.concat([df, bbands], axis=1)
    
    upper_c = f"BBU_{bb_length}_2.0"
    lower_c = f"BBL_{bb_length}_2.0"
    mid_c = f"BBM_{bb_length}_2.0"

    # 5. Dashboard Header & Metrics
    last_row = df.iloc[-1]
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Last Price", f"${last_row['close']:.3f}")
    m2.metric("RSI", f"{last_row['rsi']:.1f}")
    
    # 6. Signal Logic
    if last_row['close'] <= last_row[lower_c] and last_row['rsi'] < 35:
        st.success("🔥 SIGNAL: STRONG BUY (Silver/Oil Oversold)")
    elif last_row['close'] >= last_row[upper_c] and last_row['rsi'] > 65:
        st.error("📉 SIGNAL: STRONG SELL (Silver/Oil Overbought)")
    else:
        st.info("⚖️ SIGNAL: NEUTRAL (Market in Middle)")

    # 7. Charting with Plotly (Dark Mode)
    fig = go.Figure()

    # Candlesticks
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['open'], high=df['high'], 
        low=df['low'], close=df['close'], name="Price"
    ))

    # Bollinger Bands
    fig.add_trace(go.Scatter(x=df.index, y=df[upper_c], line=dict(color='#444'), name="Upper BB"))
    fig.add_trace(go.Scatter(x=df.index, y=df[lower_c], line=dict(color='#444'), name="Lower BB"))

    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        height=600,
        margin=dict(l=10, r=10, t=10, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Waiting for market data... check your ticker symbol.")
