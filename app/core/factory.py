from fastapi import FastAPI
from app.api import validate

def create_app() -> FastAPI:
    app = FastAPI(title="validation service")
    app.include_router(validate.router, prefix="/validate", tags=["Validation"])
    return app
