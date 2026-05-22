import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Income Predictor", layout="wide")

st.title("💰 Income Prediction (Adult Census)")
st.markdown("Predict whether income exceeds **$50K/year** using machine learning (SVC model).")

# Load model directly
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

# Input fields (same as before)
age = st.number_input("Age", min_value=17, max_value=90, value=30)
workclass = st.selectbox("Workclass", ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Without-pay", "Never-worked"])
fnlwgt = st.number_input("Fnlwgt", value=189778)
education = st.selectbox("Education", ["HS-grad", "Some-college", "Bachelors", "Masters", "Doctorate", "Assoc-acdm", "Assoc-voc", "Prof-school", "11th", "10th", "9th", "12th", "1st-4th", "5th-6th", "7th-8th", "Preschool"])
educational_num = st.number_input("Education Number", value=10)
marital_status = st.selectbox("Marital Status", ["Married-civ-spouse", "Never-married", "Divorced", "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"])
occupation = st.selectbox("Occupation", ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", "Armed-Forces"])
relationship = st.selectbox("Relationship", ["Husband", "Not-in-family", "Own-child", "Unmarried", "Wife", "Other-relative"])
race = st.selectbox("Race", ["White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"])
gender = st.selectbox("Gender", ["Male", "Female"])
capital_gain = st.number_input("Capital Gain", value=0)
capital_loss = st.number_input("Capital Loss", value=0)
hours_per_week = st.number_input("Hours per week", value=40)
native_country = st.selectbox("Native Country", ["United-States", "Canada", "Mexico", "India", "Philippines", "Germany", "Japan", "China", "Puerto-Rico", "El-Salvador", "South", "Columbia", "Vietnam", "England", "Cuba", "Jamaica", "Iran", "Honduras", "Nicaragua", "Italy", "Ecuador", "France", "Taiwan", "Portugal", "Dominican-Republic", "Peru", "Greece", "Poland", "Hungary", "Guatemala", "Ireland", "Outlying-US(Guam-USVI-etc)", "Scotland", "Thailand", "Laos", "Trinadad&Tobago", "Yugoslavia", "Hong", "Cambodia"])

if st.button("🔮 Predict"):
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
    pred = model.predict(df_input)[0]
    st.success(f"Predicted Income: **{pred}**")
