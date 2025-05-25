from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.services.auth_service.db_managers import UserManager, RoleManager


class User(Base):
    _manager_cls = UserManager

    username: Mapped[str] = mapped_column(
        String(14),
        unique=True,
        nullable=False,
    )
    password: Mapped[str]

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), nullable=True, default=1, server_default="1"
    )
    role: Mapped["Role"] = relationship("Role", back_populates="users", lazy="joined")


class Role(Base):
    _manager_cls = RoleManager
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    users: Mapped[list["User"]] = relationship(back_populates="role")


class JWTBlackList(Base):
    jti: Mapped[str] = mapped_column(unique=True, nullable=False)
    expire_at: Mapped[datetime] = mapped_column(
        DateTime
    )  # col for delete when jwt was expired
