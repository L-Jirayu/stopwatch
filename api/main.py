from fastapi import FastAPI, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# ✅ เปิดให้ทุก origin เข้าถึง
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # อนุญาตทุก origin
    allow_credentials=False,   # ต้องเป็น False ถ้าใช้ "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

QUOTABLE_API = "https://api.quotable.io/random"  # ✅ ใช้ https

# Cache เก็บคำคมและเวลาอัพเดตล่าสุด
cached_quote = None
cache_timestamp = 0
cache_ttl = 1  # วินาที

@app.get("/quote")
async def get_quote():
    global cached_quote, cache_timestamp

    now = time.time()
    if cached_quote and (now - cache_timestamp < cache_ttl):
        return cached_quote

    async with httpx.AsyncClient(timeout=5) as client:   # ✅ กัน timeout
        response = await client.get(QUOTABLE_API)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching quote")
        data = response.json()

    cached_quote = data
    cache_timestamp = now

    return data
