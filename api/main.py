from fastapi import FastAPI, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# เพิ่มโดเมน production ของ Vercel เข้าไป
origins = [
    "http://127.0.0.1:5500",                       # ใช้ตอน dev local
    "https://stopwatch-sigma-olive.vercel.app",    # production domain
    # ถ้ามี preview domains หลายอัน ใช้ regex ด้านล่างแทน
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # หรือใช้ allow_origin_regex=r"^https://.*\.vercel\.app$"
    allow_credentials=False,          # ถ้าไม่ได้ส่ง cookie -> ปิดไว้จะง่ายกว่า
    allow_methods=["*"],
    allow_headers=["*"],
)

QUOTABLE_API = "https://api.quotable.io/random"  # ใช้ https

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

    async with httpx.AsyncClient() as client:
        response = await client.get(QUOTABLE_API)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching quote")
        data = response.json()

    cached_quote = data
    cache_timestamp = now
    return data
