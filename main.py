from app.core.factory import create_app
from app.core.config import ENABLE_RATE_LIMIT
from slowapi.middleware import SlowAPIMiddleware
from app.core.limiter import limiter
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

# Создаем приложение
app = create_app()

# Настраиваем rate limiting
if ENABLE_RATE_LIMIT:
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)


    # Обработчик ошибок rate limit
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "detail": "Too many requests. Please try again later."
            }
        )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)