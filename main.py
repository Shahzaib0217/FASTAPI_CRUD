from fastapi import FastAPI
from app.routes import router as api_router
from app.db_handler import create_tables
app = FastAPI()

# Include the API router
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    create_tables()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
