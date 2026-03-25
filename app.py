import streamlit as st
from PIL import Image

st.set_page_config(page_title="Silver/Oil Signal Pro", layout="wide")

st.title("📊 Silver & Oil Live Signal Analysis")
st.sidebar.header("Trading Controls")
asset = st.sidebar.selectbox("Current Asset", ["Silver (SI=F)", "Crude Oil (CL=F)"])
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h"])

uploaded_file = st.file_uploader("📤 Upload Chart Screenshot (TradingView/MT4)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        img = Image.open(uploaded_file)
        st.image(img, caption=f"Analyzing {asset} on {timeframe}", use_container_width=True)
    
    with col2:
        st.subheader("🤖 AI Analysis Request")
        st.write("To get your Entry/Exit, copy the text below and paste it back to our chat with this screenshot:")
        
        analysis_prompt = f"""
        Analyze this {asset} chart on the {timeframe} timeframe.
        1. Identify the Market Trend (Bullish/Bearish/Sideways).
        2. Give a clear BUY or SELL signal.
        3. Provide exact Entry Point.
        4. Provide Take Profit (TP) and Stop Loss (SL).
        """
        st.code(analysis_prompt)
        
        st.info("Directly upload this image in our chat now for the live signal.")
else:
    st.info("Waiting for chart upload... Please take a screenshot of your trading platform.")
