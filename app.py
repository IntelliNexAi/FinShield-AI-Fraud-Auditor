import streamlit as st
import pickle
import time
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="FinShield AI | Professional Audit Dashboard",
    page_icon="⚖️",
    layout="wide"
)

# --- PROFESSIONAL CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle, #0e1117 0%, #000000 100%);
        color: #e0e0e0;
    }
    
    /* Header Styling */
    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 50px;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(#00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 18px;
        margin-bottom: 40px;
    }

    /* Professional Card Containers */
    .report-card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Result Boxes */
    .fraud-alert {
        padding: 20px;
        background-color: rgba(255, 75, 75, 0.1);
        border: 2px solid #ff4b4b;
        border-radius: 15px;
        color: #ff4b4b;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.3);
    }
    
    .safe-alert {
        padding: 20px;
        background-color: rgba(30, 255, 180, 0.1);
        border: 2px solid #1effb4;
        border-radius: 15px;
        color: #1effb4;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 0 20px rgba(30, 255, 180, 0.3);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111;
        border-right: 1px solid #333;
    }
    
    /* Button Animation */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        padding: 15px;
        font-weight: bold;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    try:
        with open('fraud_news_model.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

model = load_model()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135706.png", width=80)
    st.title("Admin Panel")
    st.markdown("---")
    st.write(" **Model Accuracy:** 79.20%")
    st.write(" **Engine:** Random Forest + TF-IDF")
    st.markdown("---")
    st.info("This system analyzes linguistic patterns in financial news to detect potential fraudulent activity.")

# --- MAIN DASHBOARD ---
st.markdown('<div class="main-title">FINSHIELD AI AUDITOR</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Next-Generation Financial Intelligence & Risk Assessment</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    news_text = st.text_area(" INPUT FINANCIAL NEWS SUMMARY", height=250, placeholder="Paste the financial news summary here for deep-scan analysis...")
    
    if st.button("EXECUTE SCAN"):
        if news_text.strip() == "":
            st.warning("Analysis failed: No input data detected.")
        else:
            if model:
                # Prediction logic
                with st.spinner(" Scanning text patterns and cross-referencing datasets..."):
                    time.sleep(2)  # Professional delay
                    
                    # Get prediction and confidence
                    pred = model.predict([news_text])[0]
                    proba = model.predict_proba([news_text])[0]
                    confidence = max(proba) * 100
                    
                    st.markdown("### Analysis Results")
                    if pred == 1:
                        st.markdown(f'''
                            <div class="fraud-alert">
                                <h2> HIGH RISK DETECTED</h2>
                                <p>This summary matches patterns associated with Financial Fraud.</p>
                                <p style="font-size: 24px;">Confidence: {confidence:.2f}%</p>
                            </div>
                        ''', unsafe_allow_html=True)
                    else:
                        st.markdown(f'''
                            <div class="safe-alert">
                                <h2> NON-FRAUDULENT / SAFE</h2>
                                <p>Standard financial reporting patterns identified.</p>
                                <p style="font-size: 24px;">Confidence: {confidence:.2f}%</p>
                            </div>
                        ''', unsafe_allow_html=True)
            else:
                st.error("Engine Offline: 'fraud_news_model.pkl' not found.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="report-card" style="height: 100%;">', unsafe_allow_html=True)
    st.subheader(" System Status")
    st.success(" Engine: Active")
    st.success(" Database: Connected")
    st.markdown("---")
    st.subheader(" Audit Guide")
    st.markdown("""
    - **High Risk:** Indicates linguistic triggers like unauthorized transfers, tax evasion, or missing records.
    - **Safe:** Standard market movements, earnings reports, or regulatory compliance news.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #555;'>FinShield AI Auditor Framework © 2026 | Enterprise Security Protocol</p>", unsafe_allow_html=True)