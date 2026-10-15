
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
<<<<<<< HEAD
    title="Transport Collection System ",
=======
    title="Transport Collection Management API",
>>>>>>> 11c30a2bde7d3bb21ca52142a8c66dc85b4d7cd4
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


<<<<<<< HEAD
@app.get("/", tags=["Default"])
=======
@app.get("/", tags=["Root"])
>>>>>>> 11c30a2bde7d3bb21ca52142a8c66dc85b4d7cd4
def home():
    return {
        "message": "Transport Collection API is running",
        "docs": "/docs",
    }
