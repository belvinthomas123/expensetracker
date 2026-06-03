import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "expense-tracker-secret")
    uri = os.environ.get("DATABASE_URL", "sqlite:///expenses.db")
    
    # Fix for newer SQLAlchemy versions if 'postgres://' is used instead of 'postgresql://'
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
