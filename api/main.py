from fastapi import FastAPI
from routers.screener import router as screener_router

app = FastAPI()
app.include_router(screener_router)

@app.get("/healthz")
async def health():
    return {"status": "ok"} 