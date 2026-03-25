import streamlit as st
from PIL import Image

# 1. Basic Page Config
st.set_page_config(page_title="Silver/Oil Manual Analyzer", layout="centered")

st.title("🥈 Silver & 🛢️ Oil Manual Signal Tool")
st.write("Upload your chart screenshot below for a structured Entry/Exit plan.")

# 2. Image Uploader
uploaded_file = st.file_uploader("Choose a chart screenshot...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded chart
    image = Image.open(uploaded_file)
    st.image(image, caption='Current Market View', use_container_width=True)
    
    st.divider()
    
    # 3. Manual Input Section for Strategy
    st.subheader("📝 Define Your Trade Plan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        asset = st.selectbox("Asset", ["Silver (SI)", "Crude Oil (CL)"])
        bias = st.radio("Market Bias", ["Bullish (Buy)", "Bearish (Sell)", "Neutral"])
    
    with col2:
        entry = st.number_input("Desired Entry Price", format="%.3f")
        risk_reward = st.slider("Target Risk/Reward Ratio", 1.0, 5.0, 2.0)

    # 4. Automated TP/SL Calculation Logic
    if entry > 0:
        st.markdown("### 🎯 Suggested Levels")
        
        # Simple Logic for Silver/Oil Scalping offsets
        # (Silver moves in $0.005 increments, Oil in $0.01)
        offset = 0.050 if "Silver" in asset else 0.25
        
        if bias == "Bullish (Buy)":
            sl = entry - offset
            tp = entry + (offset * risk_reward)
            st.success(f"**Action:** BUY {asset}")
        elif bias == "Bearish (Sell)":
            sl = entry + offset
            tp = entry - (offset * risk_reward)
            st.error(f"**Action:** SELL {asset}")
        else:
            st.info("Wait for a clear rejection or breakout before entering.")
            sl, tp = 0, 0

        if bias != "Neutral":
            st.write(f"**Stop Loss (SL):** {sl:.3f}")
            st.write(f"**Take Profit (TP):** {tp:.3f}")
            
    st.warning("⚠️ Remember: Scalping Silver/Oil is high risk. Always check the Economic Calendar for news spikes.")

else:
    st.info("Please upload a PNG or JPG screenshot from TradingView or MetaTrader to begin.")
