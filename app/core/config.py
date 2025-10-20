from dotenv import load_dotenv
import os

load_dotenv()

FESTU_ENDPOINT = os.getenv("FESTU_ENDPOINT")

if not FESTU_ENDPOINT:
    raise RuntimeError('FESTU_ENDPOINT not set in .env')

CACHE_TTL = int(os.getenv("CACHE_TTL", 600))
CACHE_MAXSIZE = int(os.getenv("CACHE_MAXSIZE", 100))

RATE_LIMIT = os.getenv("RATE_LIMIT", "60/hour")
ENABLE_RATE_LIMIT = os.getenv("ENABLE_RATE_LIMIT", "true").lower() == "true"