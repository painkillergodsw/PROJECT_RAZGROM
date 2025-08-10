from fastapi import APIRouter

router = APIRouter(prefix="/feroxbuster")

@router.get("/health_check")
async def health_check() -> dict:
    return {"status": "ok"}
