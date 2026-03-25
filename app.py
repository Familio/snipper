import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup API (Put your key in Streamlit Secrets or enter it here)
st.set_page_config(page_title="AI Chart Scalper", layout="wide")
st.title("🤖 AI-Powered Silver & Oil Analyzer")

api_key = st.sidebar.text_input("Enter Google API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 2. Upload Section
    uploaded_file = st.file_uploader("Upload Silver or Oil Chart", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Chart", use_container_width=True)
        
        if st.button("Analyze for Entry/Exit"):
            with st.spinner("AI is reading the chart..."):
                # 3. The Prompt that defines the logic
                prompt = """
                You are a professional commodities day trader. Analyze this chart image for Silver (SI) or Oil (CL).
                1. Identify the current Trend.
                2. Identify major Support and Resistance levels.
                3. Based on price action, give a clear BUY, SELL, or WAIT signal.
                4. Provide a specific Entry Price, Take Profit (TP), and Stop Loss (SL).
                Format the output clearly with bold headers.
                """
                
                response = model.generate_content([prompt, img])
                
                st.markdown("---")
                st.subheader("📊 Trade Plan")
                st.write(response.text)
else:
    st.warning("Please enter your Google API Key in the sidebar to start.")
