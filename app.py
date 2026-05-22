import streamlit as st
import pickle
import pandas as pd
import time

# ---------- Page Config ----------
st.set_page_config(
    page_title="Income Predictor Pro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
    /* Global styles */
    .main {
        padding: 2rem;
    }
    .title-text {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #6c757d;
        margin-bottom: 2rem;
    }
    .card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
        border: 1px solid #e9ecef;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-left: 0.5rem;
        border-left: 4px solid #667eea;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 2rem;
        padding: 0.6rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102,126,234,0.3);
    }
    .result-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 1rem;
        padding: 1.5rem;
        text-align: center;
        margin-top: 1.5rem;
    }
    .result-high {
        font-size: 2.2rem;
        font-weight: 800;
        color: #28a745;
    }
    .result-low {
        font-size: 2.2rem;
        font-weight: 800;
        color: #dc3545;
    }
    .footer {
        text-align: center;
        color: #adb5bd;
        font-size: 0.8rem;
        margin-top: 2rem;
    }
    @media (prefers-color-scheme: dark) {
        .card {
            background: #1e1e2e;
            border-color: #343a40;
        }
        .result-box {
            background: #2d2d3a;
        }
        .section-header {
            color: #f8f9fa;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<div class="title-text">💰 Income Predictor Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Demographic & employment data → Income >50K or ≤50K</div>', unsafe_allow_html=True)

# ---------- Load Model with Cache ----------
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

try:
    model = load_model()
    model_loaded = True
except FileNotFoundError:
    st.error("❌ Model file `model.pkl` not found. Please upload it to the repository.")
    model_loaded = False
    st.stop()

# ---------- Form Layout using Tabs ----------
tab1, tab2, tab3 = st.tabs(["👤 Personal Info", "💼 Work & Education", "💰 Financial"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=17, max_value=90, value=30, help="Age in years")
        gender = st.selectbox("Gender", ["Male", "Female"])
        race = st.selectbox("Race", ["White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"])
    with col2:
        relationship = st.selectbox("Relationship", ["Husband", "Not-in-family", "Own-child", "Unmarried", "Wife", "Other-relative"])
        marital_status = st.selectbox("Marital Status", ["Married-civ-spouse", "Never-married", "Divorced", "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"])

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        workclass = st.selectbox("Workclass", ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Without-pay", "Never-worked"])
        occupation = st.selectbox("Occupation", ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", "Armed-Forces"])
    with col2:
        hours_per_week = st.number_input("Hours per week", min_value=1, max_value=99, value=40, help="Average hours worked per week")
        education = st.selectbox("Education Level", ["HS-grad", "Some-college", "Bachelors", "Masters", "Doctorate", "Assoc-acdm", "Assoc-voc", "Prof-school", "11th", "10th", "9th", "12th", "1st-4th", "5th-6th", "7th-8th", "Preschool"])
        educational_num = st.number_input("Education Years", min_value=1, max_value=16, value=10, help="Number of years of education completed")

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        capital_gain = st.number_input("Capital Gain", min_value=0, max_value=100000, value=0, help="Investment income (stocks, etc.)")
        fnlwgt = st.number_input("Fnlwgt", min_value=10000, max_value=2000000, value=189778, help="Final sampling weight (demographic factor)")
    with col2:
        capital_loss = st.number_input("Capital Loss", min_value=0, max_value=5000, value=0, help="Investment losses")
        native_country = st.selectbox("Native Country", ["United-States", "Canada", "Mexico", "India", "Philippines", "Germany", "Japan", "China", "Puerto-Rico", "El-Salvador", "South", "Columbia", "Vietnam", "England", "Cuba", "Jamaica", "Iran", "Honduras", "Nicaragua", "Italy", "Ecuador", "France", "Taiwan", "Portugal", "Dominican-Republic", "Peru", "Greece", "Poland", "Hungary", "Guatemala", "Ireland", "Outlying-US(Guam-USVI-etc)", "Scotland", "Thailand", "Laos", "Trinadad&Tobago", "Yugoslavia", "Hong", "Cambodia"])

# ---------- Prediction Button ----------
center_col1, center_col2, center_col3 = st.columns([1, 2, 1])
with center_col2:
    predict_clicked = st.button("🔮 Predict Income", use_container_width=True)

# ---------- Result Display ----------
if predict_clicked:
    input_dict = {
        'age': [age],
        'workclass': [workclass],
        'fnlwgt': [fnlwgt],
        'education': [education],
        'educational-num': [educational_num],
        'marital-status': [marital_status],
        'occupation': [occupation],
        'relationship': [relationship],
        'race': [race],
        'gender': [gender],
        'capital-gain': [capital_gain],
        'capital-loss': [capital_loss],
        'hours-per-week': [hours_per_week],
        'native-country': [native_country]
    }
    df_input = pd.DataFrame(input_dict)

    with st.spinner("Analyzing your data..."):
        time.sleep(0.5)  # slight delay for better UX
        prediction = model.predict(df_input)[0]

    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    if prediction == ">50K":
        st.markdown(f'<div class="result-high">✅ HIGH INCOME (>50K)</div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown(f'<div class="result-low">⚠️ LOW INCOME (≤50K)</div>', unsafe_allow_html=True)
    st.markdown('<p style="margin-top: 0.5rem;">Based on SVC model with 86.29% accuracy</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("---")
st.markdown('<div class="footer">🏆 Best Model: SVC | Accuracy: 86.29% | Built with Streamlit & Scikit-learn</div>', unsafe_allow_html=True)
