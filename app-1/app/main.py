from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import init_db
from . import crud, schemas, deps, models

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()
    print("Database tables created!")

@app.get("/")
def read_root():
    return {"status":"ok", "msg":"hello"}

# 1. Sign up a new user
@app.post("/users/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# 2. Get user details by ID
@app.get("/users/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(deps.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
