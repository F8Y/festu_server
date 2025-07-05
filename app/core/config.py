from dotenv import load_dotenv
import os

load_dotenv()

FESTU_ENDPOINT = os.getenv("FESTU_ENDPOINT")

if not FESTU_ENDPOINT:
    raise RuntimeError('FESTU_ENDPOINT not set in .env')
