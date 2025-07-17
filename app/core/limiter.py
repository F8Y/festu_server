from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import RATE_LIMIT

limiter = Limiter(key_func=get_remote_address, default_limits=[RATE_LIMIT])