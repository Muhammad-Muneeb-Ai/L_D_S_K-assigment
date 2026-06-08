import pickle
from pathlib import Path
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Load model
model_path = Path(__file__).resolve().parent / "model.pkl"
try:
    with model_path.open("rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError(f"Model file not found: {model_path}")
except Exception as exc:
    raise RuntimeError(f"Unable to load model: {exc}") from exc

# Input features (same as training)
class InputData(BaseModel):
    age: int
    workclass: str
    fnlwgt: int
    education: str
    educational_num: int
    marital_status: str
    occupation: str
    relationship: str
    race: str
    gender: str
    capital_gain: int
    capital_loss: int
    hours_per_week: int
    native_country: str

@app.post("/predict")
def predict(data: InputData):
    input_dict = {
        "age": [data.age],
        "workclass": [data.workclass],
        "fnlwgt": [data.fnlwgt],
        "education": [data.education],
        "educational-num": [data.educational_num],
        "marital-status": [data.marital_status],
        "occupation": [data.occupation],
        "relationship": [data.relationship],
        "race": [data.race],
        "gender": [data.gender],
        "capital-gain": [data.capital_gain],
        "capital-loss": [data.capital_loss],
        "hours-per-week": [data.hours_per_week],
        "native-country": [data.native_country],
    }
    df = pd.DataFrame(input_dict)
    pred = model.predict(df)[0]
    return {"prediction": pred}

@app.get("/")
def home():
    return {"message": "Income Prediction API"}
