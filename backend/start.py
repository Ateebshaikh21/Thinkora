#!/usr/bin/env python3
"""
Thinkora Backend Startup Script
"""
import uvicorn
import logging
from main import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    print("🚀 Starting Thinkora Backend Server...")
    print("📚 Your Smart Study Assistant is ready!")
    print("🌐 API Documentation: http://localhost:8000/docs")
    print("💡 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )