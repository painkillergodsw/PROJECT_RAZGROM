from fastapi import APIRouter, BackgroundTasks
from subfinder.subfinder import SDK

import time
router = APIRouter(prefix="/subfinder")

@router.get("/health_check")
async def health_check() -> dict:
    return {"status": "ok"}


@router.get("/test_background_task")
async def bg_task_test() -> dict:
    start_time = time.perf_counter()

    subfinder = SDK()
    result = await subfinder.scan_domain("punkration.ru")
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    return {
        "result": result,
        "execution_time_seconds": execution_time
    }