from sqlalchemy import Column, Integer, String, Float, DateTime, Text
import datetime
from database import Base

class MatchRecord(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    producer_id = Column(String, index=True)
    producer_name = Column(String)
    consumer_id = Column(String, index=True)
    consumer_name = Column(String)
    
    waste_type = Column(String)
    quantity = Column(Float)
    unit = Column(String)
    
    distance_km = Column(Float)
    
    agreement_json = Column(Text)  # JSON string from Negotiator
    sustainability_pitch = Column(Text)  # String from Evaluator
