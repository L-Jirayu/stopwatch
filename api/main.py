from fastapi import FastAPI, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# ตั้งค่า CORS อนุญาต frontend ที่รันบน localhost:5500 เรียกได้
origins = [
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

QUOTABLE_API = "http://api.quotable.io/random"

# Cache เก็บคำคมและเวลาอัพเดตล่าสุด
cached_quote = None
cache_timestamp = 0
cache_ttl = 1

@app.get("/quote")
async def get_quote():
    global cached_quote, cache_timestamp

    now = time.time()
    if cached_quote and (now - cache_timestamp < cache_ttl):
        return cached_quote

    async with httpx.AsyncClient() as client:
        response = await client.get(QUOTABLE_API)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching quote")
        data = response.json()

    cached_quote = data
    cache_timestamp = now

    return data
