from fastapi import FastAPI
from alerts_ai.features.alerts.router import router as alerts_router

app = FastAPI()

app.include_router(alerts_router)

@app.get("/health")
async def health():
    return {"status": "ok"}