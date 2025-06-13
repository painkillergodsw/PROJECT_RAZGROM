from fastapi import APIRouter, Depends
from schemas import UserSchema
from depends import get_user

router = APIRouter(prefix="/core")


@router.post("/create-project")
async def index(user: UserSchema = Depends(get_user)):
    return user


@router.get("/health_check")
async def health_check() -> dict:
    return {"status": "ok"}
