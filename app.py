import streamlit as st
from google import genai
from PIL import Image
import os

st.set_page_config(page_title="AI Silver/Oil Scalper", layout="wide")
st.title("🤖 AI Commodity Chart Analyzer")

# Use a sidebar for the API key for security
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    # New 2026 SDK Client initialization
    client = genai.Client(api_key=api_key)
    
    uploaded_file = st.file_uploader("Upload Silver (SI) or Oil (CL) Chart", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Target Chart", use_container_width=True)
        
        if st.button("Generate Buy/Sell Signal"):
            with st.spinner("Analyzing market structure..."):
                prompt = """
                Identify if this is Silver or Oil. 
                1. Determine the current Trend (Bullish/Bearish).
                2. Give a clear 'BUY' or 'SELL' or 'WAIT' signal.
                3. Provide exact levels for: ENTRY, TAKE PROFIT, and STOP LOSS.
                Use bold formatting for the signal.
                """
                
                # Using the latest 2026 model 'gemini-3-flash'
                response = client.models.generate_content(
                    model='gemini-3-flash',
                    contents=[img, prompt]
                )
                
                st.markdown("---")
                st.subheader("🎯 Trade Execution Plan")
                st.write(response.text)
else:
    st.info("Please enter your API Key in the sidebar to activate the AI.")
