from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class AIModelDB(Base):
    __tablename__ = "ai_models" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    framework = Column(String)
    accuracy = Column(Float)
    is_ready = Column(Boolean, default=False)