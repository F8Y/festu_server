from cachetools import TTLCache
from app.core.config import CACHE_TTL, CACHE_MAXSIZE

schedule_cache = TTLCache(maxsize=CACHE_MAXSIZE, ttl=CACHE_TTL)