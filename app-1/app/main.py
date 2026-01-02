from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import init_db
from . import crud, schemas, deps, models
from fastapi.security import OAuth2PasswordRequestForm
from . import auth

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

# 3. Login and get JWT token
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)):
    # 1. find the user by email
    user = crud.get_user_by_email(db, email=form_data.username) # OAuth2 در فیلد username ایمیل را می‌فرستد
    
    # 2. Check password
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # 3. create access token
    access_token = auth.create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

# Test endpoint to get current user
@app.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


# app/main.py
from .auth import get_current_user

# 
@app.post("/models/", status_code=status.HTTP_201_CREATED)
def create_ai_model(
    model: schemas.AIModel,  # اضافه کردن schemas. قبل از نام کلاس
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(deps.get_db)
):
    return {
        "message": f"Model {model.name} created successfully by {current_user.email}",
        "data": model
    }

@app.get("/users/", response_model=list[schemas.UserOut])
def read_all_users(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(get_current_user) 
):
    return db.query(models.User).all()