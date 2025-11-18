from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

from routes.subjects import router as subjects_router
from routes.analysis import router as analysis_router
from routes.explanations import router as explanations_router
from routes.quiz import router as quiz_router
from database.db_connection import connect_to_mongo

app = FastAPI(
    title="Thinkora API",
    description="Smart Study Assistant Backend",
    version="1.0.0"
)

# CORS configuration - supports both development and production
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:5173,https://frontend-gnievugal-ateebshaikh0821-8173s-projects.vercel.app,https://frontend-nprnofldn-ateebshaikh0821-8173s-projects.vercel.app,https://frontend-oayap1b1e-ateebshaikh0821-8173s-projects.vercel.app,https://frontend-ccbl7kahd-ateebshaikh0821-8173s-projects.vercel.app")
allowed_origins = [origin.strip() for origin in cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(subjects_router, prefix="/api/subjects", tags=["subjects"])
app.include_router(analysis_router, prefix="/api/analysis", tags=["analysis"])
app.include_router(explanations_router, prefix="/api/explanations", tags=["explanations"])
app.include_router(quiz_router, prefix="/api/quiz", tags=["quiz"])

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    try:
        await connect_to_mongo()
        print("✅ Connected to MongoDB successfully")
    except Exception as e:
        print(f"⚠️  MongoDB connection failed: {e}")
        print("🔄 Running in development mode without database")

@app.get("/")
async def root():
    return {"message": "Welcome to Thinkora API - Your Smart Study Assistant"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Thinkora Backend"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)