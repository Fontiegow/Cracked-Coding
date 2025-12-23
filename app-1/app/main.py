# app/main.py
from fastapi import FastAPI
from fastapi import FastAPI
from app.models import AIModelDB 
from app.database import init_db

app = FastAPI()
@app.get("/")
def read_root():
    return {"status":"ok", "msg":"hello"}

from pydantic import BaseModel

class AIModel(BaseModel):
    name: str
    framework: str 
    accuracy: float # e.g., 0.95 for 95%

@app.post("/models/")
def create_model(model: AIModel):
    return {"message": "Success", "data": model}


#app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()
    print("Database tables created!")
