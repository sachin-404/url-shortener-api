from sqlalchemy import Column, String, Integer, Boolean
from .database import Base

class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    secret_key = Column(String, unique=True, index=True)
    input_url = Column(String, index=True)
    is_active= Column(Boolean, default=True)
    clicks = Column(Integer, default=0)
    