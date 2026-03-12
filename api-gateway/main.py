import os
import sys
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging

# Set up global sys.path for microservices as namespace packages
import sys
import os
for svc in ['financial-service', 'revenue-service', 'operations-service', 'assets-service', 'auth-service']:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), f"../services/{svc}"))

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../db-schemas'))
from database import engine, Base

from routers.v1 import auth, financial, revenue, operations, assets

# Create FastAPI app
app = FastAPI(
    title="Gram Panchayat API",
    version="1.0.0",
    description="Modular Gram Panchayat Namunas Management System",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(financial.router, prefix="/api/v1/financial", tags=["Financial"])
app.include_router(revenue.router, prefix="/api/v1/revenue", tags=["Revenue"])
app.include_router(operations.router, prefix="/api/v1/operations", tags=["Operations"])
app.include_router(assets.router, prefix="/api/v1/assets", tags=["Assets"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Gram Panchayat API - Modular Architecture",
        "version": "1.0.0",
        "docs": "/api/docs",
        "modules": {
            "database": "db-schemas",
            "gateway": "api-gateway",
            "services": ["auth", "financial", "revenue", "operations", "assets", "reports"]
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@app.get("/api/info")
async def api_info():
    """API information"""
    return {
        "architecture": "Modular Microservices",
        "modules": {
            "db-schemas": "Database layer with 44 SQLAlchemy models",
            "api-gateway": "FastAPI entry point with routing",
            "auth-service": "Authentication and user management",
            "financial-service": "Budget, cashbook, accounts (Namunas 1-6)",
            "revenue-service": "Receipts, property tax, demands (Namunas 7-13)",
            "operations-service": "Purchases, employees, salaries (Namunas 15-24)",
            "assets-service": "Assets, properties, work estimates (Namunas 19, 23, 25-27)",
            "reports-service": "PDF and Excel report generation"
        },
        "total_namunas": 33,
        "total_models": 44
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
