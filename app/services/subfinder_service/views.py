from fastapi import APIRouter, BackgroundTasks
from subfinder.subfinder import SDK

import time
router = APIRouter(prefix="/subfinder")

@router.get("/health_check")
async def health_check() -> dict:
    return {"status": "ok"}
