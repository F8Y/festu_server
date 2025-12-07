from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api import institutes, schedule
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI(
        title="FESTU Schedule API",
        description="API для получения расписания",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    origins = [
        'http://localhost:3000',
        'http://127.0.0.1:3000'
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(
        institutes.router,
        prefix="/api/v1/institutes",
        tags=["Institutes"]
    )

    app.include_router(
        schedule.router,
        prefix="/api/v1/schedule",
        tags=["Schedule"]
    )

    @app.get("/health", tags=["System"])
    async def health_check():
        return JSONResponse(
            content={
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0"
            }
        )

    @app.get("/", tags=["System"])
    async def root():
        return {
            "message": "FESTU Schedule API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/health",
            "endpoints": {
                "institutes": "/api/v1/institutes",
                "groups": "/api/v1/institutes/{institute_id}/groups",
                "schedule": "/api/v1/schedule?group_id={id}&Time={dd.mm.yyyy}"
            }
        }

    return app
