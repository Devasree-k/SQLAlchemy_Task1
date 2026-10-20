
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database.base import Base
from database.connection import engine

# Import models so SQLAlchemy registers both tables.
from models.driver_model import Driver
from models.transport_collection_model import TransportCollection

from routers.driver_router import router as driver_router
from routers.transport_collection_router import (
    router as collection_router,
)
from exceptions.transport_collection_exception import (
    NotFoundException,
    ConflictException,
    BadRequestException,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Transport Collection API",
    description="Relationship-based Driver and Collection Management",
    version="2.0.0",
    lifespan=lifespan,
)

@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(ConflictException)
async def conflict_handler(request: Request, exc: ConflictException):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(BadRequestException)
async def bad_request_handler(request: Request, exc: BadRequestException):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

app.include_router(driver_router)
app.include_router(collection_router)

@app.get("/")
def home():
    return {
        "message": "Transport Collection API is running",
        "docs": "/docs",
    }
