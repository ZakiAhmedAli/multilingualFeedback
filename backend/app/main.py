import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
import json

# Load environment variables
load_dotenv()

# --- Gemini AI Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
# /app/app/main.py
model = genai.GenerativeModel('gemini-1.0-pro')

# --- Database Configuration ---
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Database Model (SQLAlchemy) ---
class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=True)
    sentiment = Column(String(50), nullable=True)
    language = Column(String(50), nullable=True)
    product = Column(String(100), nullable=True, index=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

# --- Pydantic Schemas (for API data validation) ---
class FeedbackCreate(BaseModel):
    text: str
    product: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    original_text: str
    translated_text: Optional[str] = None
    sentiment: Optional[str] = None
    language: Optional[str] = None
    product: Optional[str] = None

    class Config:
        orm_mode = True

class StatsResponse(BaseModel):
    total_feedback: int
    positive_percentage: float
    negative_percentage: float
    neutral_percentage: float

# --- FastAPI App Initialization ---
app = FastAPI(title="Multilingual Customer Feedback Analyzer")

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Gemini Helper Function ---
def analyze_text_with_gemini(text: str):
    """Uses Gemini to detect language, translate, and classify sentiment."""
    prompt = f"""
    Analyze the following customer feedback text. Provide the response as a valid JSON object with three keys: "language", "translated_text", and "sentiment".
    1.  "language": The detected language of the text.
    2.  "translated_text": Translate the text into English.
    3.  "sentiment": Classify the sentiment as "positive", "negative", or "neutral".

    Text: "{text}"
    """
    try:
        response = model.generate_content(prompt)
        # Clean up the response to get a valid JSON
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"Gemini analysis failed: {e}")
        # Provide a fallback in case of API error
        return {"language": "unknown", "translated_text": text, "sentiment": "neutral"}


# --- API Endpoints ---
@app.post("/api/feedback", response_model=FeedbackResponse, status_code=201)
def submit_feedback(feedback_data: FeedbackCreate, db: Session = Depends(get_db)):
    """Accepts new customer feedback, analyzes it, and stores it."""
    # 1. Analyze with Gemini [cite: 7]
    analysis = analyze_text_with_gemini(feedback_data.text)

    # 2. Create a new feedback record
    db_feedback = Feedback(
        original_text=feedback_data.text,
        translated_text=analysis.get("translated_text"),
        sentiment=analysis.get("sentiment"),
        language=analysis.get("language"),
        product=feedback_data.product
    )

    # 3. Save to database
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@app.get("/api/feedback", response_model=List[FeedbackResponse])
def get_all_feedback(product: Optional[str] = None, language: Optional[str] = None, db: Session = Depends(get_db)):
    """Retrieves all feedback, with optional filtering by product or language.""" [cite: 9]
    query = db.query(Feedback)
    if product:
        query = query.filter(Feedback.product == product)
    if language:
        query = query.filter(Feedback.language == language)
    return query.order_by(Feedback.id.desc()).all()

@app.get("/api/stats", response_model=StatsResponse)
def get_sentiment_stats(db: Session = Depends(get_db)):
    """Calculates and returns sentiment statistics."""
    total = db.query(Feedback).count()
    if total == 0:
        return {"total_feedback": 0, "positive_percentage": 0, "negative_percentage": 0, "neutral_percentage": 0}

    positive_count = db.query(Feedback).filter(Feedback.sentiment == "positive").count()
    negative_count = db.query(Feedback).filter(Feedback.sentiment == "negative").count()
    neutral_count = db.query(Feedback).filter(Feedback.sentiment == "neutral").count()

    return {
        "total_feedback": total,
        "positive_percentage": round((positive_count / total) * 100, 2),
        "negative_percentage": round((negative_count / total) * 100, 2),
        "neutral_percentage": round((neutral_count / total) * 100, 2),
    }
