from fastapi import status, HTTPException

UserAlreadyExistsHTTPException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
)

UnAuthHTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверное имя пользователя или пароль",
)

TokenNotProvideHTTPException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Токен отсутствует в заголовке или теле запроса",
)

TokenExpiredHTTPException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Время жизни токена истекло",
)

WrongTokenHTTPException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Токен не верен",
)


UserNotExistsHTTPException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
)

UserAlreadyLogoutHTTPException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Токен помечен как недействительный",
)
