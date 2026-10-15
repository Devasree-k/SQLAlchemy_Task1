from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions.transport_collection_exception import AppException
from routers.transport_collection_router import router as collection_router


app = FastAPI(
    title="Transport Collection System ",
    description=(
        "Manage daily transport collections "
    ),
    version="1.0.0"
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException, ):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )


app.include_router(collection_router)


@app.get("/")
def home():
    return {
        "message": "Transport Collection System."
    }
