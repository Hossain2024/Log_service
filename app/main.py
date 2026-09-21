from fastapi import FastAPI

from app.database import Base, engine
from app.routers.logs import router as logs_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Log Processing Service",
    description="A REST API for ingesting and retrieving application logs",
    version="1.0.0"
)

app.include_router(logs_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}