from fastapi import APIRouter

router = APIRouter(prefix="/core")


@router.get("/create-project")
async def index():
    return {"message": "Welcome to the Core API!"}


@router.get("/health_check")
async def health_check() -> dict:
    return {"status": "ok"}
