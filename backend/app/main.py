from fastapi import FastAPI

from app.api.patients import router as patients_router


app = FastAPI(
    title="AI Healthcare Security Lab",
    description="Intentionally vulnerable AI healthcare platform",
    version="1.0.0"
)


@app.get("/")
def root():

    return {
        "application": "AI Healthcare Security Lab",
        "status": "running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


app.include_router(
    patients_router
)