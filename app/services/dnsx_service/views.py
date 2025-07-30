from fastapi import APIRouter
from dnsx.tasks import scan_domains
router = APIRouter(prefix="/dnsx")

@router.get("/health_check")
async def health_check() -> dict:
    return {"status": "ok"}

@router.get("/test")
async def health_check() -> dict:
    result = await scan_domains(["punkration.ru"])
    return result