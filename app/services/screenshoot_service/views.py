from fastapi import APIRouter

router = APIRouter(prefix="/nmap")

@router.get("/health_check")
async def health_check() -> dict:
    return {"status": "ok"}
