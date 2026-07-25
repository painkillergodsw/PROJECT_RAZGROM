from fastapi import APIRouter

router = APIRouter(prefix="/katana")

@router.get("/health_check")
async def health_check() -> dict:
    return {"status": "ok"}
