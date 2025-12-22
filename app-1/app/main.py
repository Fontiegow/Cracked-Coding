# app/main.py
from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root():
    return {"status":"ok", "msg":"hello"}

from pydantic import BaseModel

class AIModel(BaseModel):
    name: str
    framework: str 
    accuracy: float # این باید عدد باشد

@app.post("/models/")
def create_model(model: AIModel):
    return {"message": "Success", "data": model}