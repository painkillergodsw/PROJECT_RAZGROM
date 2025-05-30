from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
)

UnAuthException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверное имя пользователя или пароль",
)

TokenNotProvideException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Токен отсутствует в заголовке или теле запроса",
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Время жизни токена истекло",
)

WrongTokenException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Токен не верен",
)


UserNotExistsException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
)

UserAlreadyLogout = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Токен помечен как недействительный",
)


class UserAlreadyLogoutEx(Exception):
    pass
