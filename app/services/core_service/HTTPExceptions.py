from fastapi import status, HTTPException


UserAlreadyLogoutHTTPException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Токен помечен как недействительный",
)
