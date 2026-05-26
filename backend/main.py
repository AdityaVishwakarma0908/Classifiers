from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.model_utils import process_and_predict
from typing import List

app = FastAPI(title="Digit Classifier API")

# Update ONLY this part:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://adityavishwakarma0908.github.io", "https://adityavishwakarma0908.github.io/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Keep these exactly as they were!
class ImageData(BaseModel):
    pixels: List[int]

@app.post("/predict")
async def predict_digit(data: ImageData):
    # Keep your logic here so the model actually runs!
    prediction = process_and_predict(data.pixels)
    return {"prediction": prediction}