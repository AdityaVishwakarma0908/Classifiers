from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.model_utils import process_and_predict
from typing import List

app = FastAPI(title="Digit Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Changed from a string to a List of integers!
class ImageData(BaseModel):
    pixels: List[int]

@app.post("/predict")
async def predict_digit(data: ImageData):
    try:
        prediction = process_and_predict(data.pixels)
        return {"success": True, "prediction": prediction}
    except Exception as e:
        return {"success": False, "error": str(e)}