from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.screener import router as screener_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(screener_router)

@app.get("/healthz")
async def health():
    return {"status": "ok"} 