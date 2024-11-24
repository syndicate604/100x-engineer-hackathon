from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    competitive_intelligence,
    market_expansion,
    product_evolution,
    users,
    market_analysis,
    customer_discovery,
)

from app.db import Base, create_database_engine
from app.config import get_settings


def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    # Create database tables
    settings = get_settings()
    engine = create_database_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    # Initialize FastAPI app
    app = FastAPI(
        title="Market Intelligence Platform",
        description="Comprehensive market research and business intelligence tool",
        version="0.1.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    # Include routers
    app.include_router(competitive_intelligence.router)
    app.include_router(market_expansion.router)
    app.include_router(product_evolution.router)
    app.include_router(users.router)
    app.include_router(market_analysis.router)
    app.include_router(customer_discovery.router)

    return app


app = create_application()
