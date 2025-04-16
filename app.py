from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi import Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

# Load model and feature names
model = joblib.load("diabetes_model.pkl")
feature_names = joblib.load("feature_names.pkl")

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins or specify your frontend URL, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods like GET, POST, etc.
    allow_headers=["*"],  # Allows all headers
)

# Define request body structure
class DiabetesInput(BaseModel):
    data: list[float]  # A list of 10 floats

@app.get("/")
def home():
    return {"message": "Welcome to the Diabetes Prediction API!"}

@app.post("/predict")
def predict(input: DiabetesInput, db: Session = Depends(get_db)):
    try:
        data_array = np.array(input.data).reshape(1, -1)
        prediction = model.predict(data_array)[0]

        # Save to database
        prediction_entry = models.Prediction(
            feature_0=input.data[0],
            feature_1=input.data[1],
            feature_2=input.data[2],
            feature_3=input.data[3],
            feature_4=input.data[4],
            feature_5=input.data[5],
            feature_6=input.data[6],
            feature_7=input.data[7],
            feature_8=input.data[8],
            feature_9=input.data[9],
            result=int(prediction)
        )
        db.add(prediction_entry)
        db.commit()
        db.refresh(prediction_entry)

        return {
            "id": prediction_entry.id,
            "prediction": int(prediction),
            "meaning": "Diabetic" if prediction == 1 else "Non-Diabetic"
        }

    except Exception as e:
        return {"error": str(e)}




from typing import List
from pydantic import BaseModel

# Response schema
class PredictionOut(BaseModel):
    id: int
    feature_0: float
    feature_1: float
    feature_2: float
    feature_3: float
    feature_4: float
    feature_5: float
    feature_6: float
    feature_7: float
    feature_8: float
    feature_9: float
    result: int

    class Config:
        orm_mode = True

@app.get("/records", response_model=List[PredictionOut])
def get_records(db: Session = Depends(get_db)):
    records = db.query(models.Prediction).all()
    return records