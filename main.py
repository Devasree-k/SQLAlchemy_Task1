
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from database.connection import engine
from exceptions.transport_collection_exception import AppException
from routers.transport_collection_router import router as collection_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Check the database connection at startup.
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    yield

    # Release pooled database connections at shutdown.
    engine.dispose()


app = FastAPI(
    title="Transport Collection System ",
    description=(
        "Manage daily transport collections, calculate totals, "
        "paginate records and upload reports."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


app.include_router(collection_router)


@app.get("/", tags=["Default"])
def home():
    return {
        "message": "Transport Collection API is running",
        "docs": "/docs",
    }
