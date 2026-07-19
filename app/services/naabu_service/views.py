from fastapi import APIRouter

router = APIRouter(prefix="/naabu")

@router.get("/health_check")
async def health_check() -> dict:
    return {"status": "ok"}
