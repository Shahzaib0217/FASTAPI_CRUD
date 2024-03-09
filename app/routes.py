from fastapi import APIRouter, HTTPException, File, UploadFile
from app.db_handler import SessionLocal
from app.model import Sentiments
from app.schema import SentimentsCreate, SentimentsUpdate
from app.utils import predict_sentiment

router = APIRouter()


# Predict sentiment for the input text
@router.post("/predict")
async def predict(text: str):
    sentiment = predict_sentiment(text)
    return {"sentiment": sentiment}


# Insert a new sentiment record into the database
@router.post("/insert", response_model=SentimentsCreate)
async def insert_sentiment(sentiment_data: SentimentsCreate):
    db = SessionLocal()
    db_sentiment = Sentiments(**sentiment_data.dict())
    db.add(db_sentiment)
    db.commit()
    db.refresh(db_sentiment)
    return db_sentiment


# Delete a sentiment record from the database based on comment_id
@router.delete("/delete/{comment_id}")
async def delete_sentiment(comment_id: int):
    db = SessionLocal()
    db_sentiment = db.query(Sentiments).filter(Sentiments.comment_id == comment_id).first()
    if db_sentiment:
        db.delete(db_sentiment)
        db.commit()
        return {"message": "Sentiment deleted successfully"}
    raise HTTPException(status_code=404, detail="Sentiment not found")


# Update a sentiment record in the database based on comment_id
@router.put("/update/{comment_id}", response_model=SentimentsUpdate)
async def update_sentiment(comment_id: int, sentiment_data: SentimentsUpdate):
    db = SessionLocal()
    db_sentiment = db.query(Sentiments).filter(Sentiments.comment_id == comment_id).first()
    if db_sentiment:
        for key, value in sentiment_data.dict().items():
            setattr(db_sentiment, key, value)
        db.commit()
        db.refresh(db_sentiment)
        return db_sentiment
    raise HTTPException(status_code=404, detail="Sentiment not found")


# Bulk insert sentiment records from a CSV file
@router.post("/bulk_insert")
async def bulk_insert(file: UploadFile = File(...)):
    contents = await file.read()
    rows = contents.decode().split("\n")
    records = []
    for row in rows:
        columns = row.split(",")
        if len(columns) == 3:
            print(columns)
            sentiment = predict_sentiment(columns[2])
            try:
                # Convert comment_id to integer if it's a valid integer string
                com_id = int(columns[1])
            except ValueError:
                # Handle the case where comment_id is not a valid integer
                # You can choose to skip this record or handle it differently
                print(f"Invalid comment_id: {columns[1]}")
                continue
            record = SentimentsCreate(campaign_id=columns[0], comment_id=com_id, description=columns[2], sentiment=sentiment[0]['label'])
            records.append(record)
    # Bulk insert records
    db = SessionLocal()
    try:
        db.bulk_insert_mappings(Sentiments, [record.dict() for record in records])
        db.commit()
    finally:
        db.close()
    return {"message": "Bulk insert successful"}
