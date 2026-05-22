import streamlit as st
import requests
import json
import time

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="Income Predictor Pro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Custom CSS for Professional Look ----------
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 2rem;
    }
    
    /* Title styling */
    .title-text {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Card styling for sections */
    .card {
        background: #ffffff;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border: 1px solid #e0e0e0;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #333;
        border-left: 4px solid #667eea;
        padding-left: 0.75rem;
        margin-bottom: 1rem;
    }
    
    /* Predict button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem;
        font-size: 1.1rem;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.4);
    }
    
    /* Result box */
    .result-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-radius: 1rem;
        padding: 1.5rem;
        text-align: center;
        margin-top: 1.5rem;
        border: 1px solid #667eea30;
    }
    .result-text {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    .result-subtext {
        font-size: 0.9rem;
        color: #666;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #888;
        font-size: 0.8rem;
    }
    
    /* Dark mode override for cards */
    @media (prefers-color-scheme: dark) {
        .card {
            background: #1e1e2e;
            border-color: #333;
        }
        .section-header {
            color: #eee;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<div class="title-text">💰 Income Prediction Pro</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">Predict whether income exceeds $50K/year based on demographic and employment data</p>', unsafe_allow_html=True)
st.markdown("---")

# ---------- API URL (Change when deployed) ----------
# For local testing
API_URL = "http://localhost:8000/predict"
# For production, change to your deployed Render URL
# API_URL = "https://your-api.onrender.com/predict"

# ---------- Create Form with Tabs ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

# Create tabs for better organization
tab1, tab2, tab3 = st.tabs(["👤 Personal Info", "💼 Employment", "💰 Financial"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=17, max_value=90, value=30, help="Age in years")
        gender = st.selectbox("Gender", ["Male", "Female"])
        race = st.selectbox("Race", ["White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"])
    with col2:
        relationship = st.selectbox("Relationship Status", ["Husband", "Not-in-family", "Own-child", "Unmarried", "Wife", "Other-relative"])
        marital_status = st.selectbox("Marital Status", ["Married-civ-spouse", "Never-married", "Divorced", "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"])
        education = st.selectbox("Education Level", ["HS-grad", "Some-college", "Bachelors", "Masters", "Doctorate", "Assoc-acdm", "Assoc-voc", "Prof-school", "11th", "10th", "9th", "12th", "1st-4th", "5th-6th", "7th-8th", "Preschool"])

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        workclass = st.selectbox("Workclass", ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Without-pay", "Never-worked"])
        occupation = st.selectbox("Occupation", ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", "Armed-Forces"])
    with col2:
        hours_per_week = st.number_input("Hours per week", min_value=1, max_value=99, value=40, help="Average hours worked per week")
        educational_num = st.number_input("Education Num (years)", min_value=1, max_value=16, value=10, help="Years of education completed")
        native_country = st.selectbox("Native Country", ["United-States", "Canada", "Mexico", "India", "Philippines", "Germany", "Japan", "China", "Puerto-Rico", "El-Salvador", "South", "Columbia", "Vietnam", "England", "Cuba", "Jamaica", "Iran", "Honduras", "Nicaragua", "Italy", "Ecuador", "France", "Taiwan", "Portugal", "Dominican-Republic", "Peru", "Greece", "Poland", "Hungary", "Guatemala", "Ireland", "Outlying-US(Guam-USVI-etc)", "Scotland", "Thailand", "Laos", "Trinadad&Tobago", "Yugoslavia", "Hong", "Cambodia"])

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        capital_gain = st.number_input("Capital Gain", min_value=0, max_value=100000, value=0, help="Investment income from stocks, etc.")
        fnlwgt = st.number_input("Fnlwgt (Demographic Weight)", min_value=10000, max_value=2000000, value=189778, help="Final sampling weight")
    with col2:
        capital_loss = st.number_input("Capital Loss", min_value=0, max_value=5000, value=0, help="Losses from investments")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Predict Button ----------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_clicked = st.button("🔮 Predict Income", use_container_width=True)

# ---------- Prediction Logic ----------
if predict_clicked:
    # Prepare payload
    payload = {
        "age": age,
        "workclass": workclass,
        "fnlwgt": fnlwgt,
        "education": education,
        "educational_num": educational_num,
        "marital_status": marital_status,
        "occupation": occupation,
        "relationship": relationship,
        "race": race,
        "gender": gender,
        "capital_gain": capital_gain,
        "capital_loss": capital_loss,
        "hours_per_week": hours_per_week,
        "native_country": native_country
    }
    
    # Show loading spinner
    with st.spinner("Analyzing your data..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()["prediction"]
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                if result == ">50K":
                    st.markdown('<p class="result-text" style="color: #28a745;">✅ HIGH INCOME (>50K)</p>', unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.markdown('<p class="result-text" style="color: #dc3545;">⚠️ LOW INCOME (≤50K)</p>', unsafe_allow_html=True)
                st.markdown('<p class="result-subtext">This prediction is based on the Adult Census dataset and machine learning model (SVC) with 86.29% accuracy.</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API server. Make sure FastAPI is running at http://localhost:8000")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

# ---------- Footer ----------
st.markdown("---")
st.markdown('<div class="footer">🏆 Best Model: SVC | Accuracy: 86.29% | Built with Streamlit & FastAPI</div>', unsafe_allow_html=True)