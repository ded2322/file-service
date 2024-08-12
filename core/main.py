from fastapi import FastAPI

from core.http_load.router import router as http_router
from core.streaming_load.router import router as streaming_router

app = FastAPI(
    title="Upload file service",
    version="1.0",
    description="Service for uploading files",
)


app.include_router(http_router)
app.include_router(streaming_router)
