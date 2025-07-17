from app.core.factory import create_app
from app.core.config import ENABLE_RATE_LIMIT
from fastapi import Request
from slowapi.middleware import SlowAPIMiddleware
from app.core.limiter import limiter

app = create_app()

if ENABLE_RATE_LIMIT:
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)