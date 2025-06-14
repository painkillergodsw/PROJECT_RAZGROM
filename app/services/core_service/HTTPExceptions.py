from fastapi import status, HTTPException


UserAlreadyLogoutHTTPException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Токен помечен как недействительный",
)

project_not_exists = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Проект не найден",
)
