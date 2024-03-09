from sqlalchemy import Column, Integer, String, Text
from app.db_handler import Base

class Sentiments(Base):
    __tablename__ = "sentiments"
    campaign_id = Column(String)
    comment_id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    sentiment = Column(String)
