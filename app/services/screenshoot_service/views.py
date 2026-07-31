from fastapi import APIRouter

router = APIRouter(prefix="/screenshoot")

@router.get("/health_check")
async def health_check() -> dict:
    return {"status": "ok"}
