import sys
from fastapi import FastAPI
from backend.retrieve.retrieve_router import router as retrieve_router

app = FastAPI(title="YouTube Video Recommendation API")

app.include_router(retrieve_router, prefix="/retrieve", tags=["retrieve"])

@app.on_event("startup")  # Add this startup event
async def startup_event():
    print(f"Running FastAPI with Python: {sys.executable}")  # Print Python path
