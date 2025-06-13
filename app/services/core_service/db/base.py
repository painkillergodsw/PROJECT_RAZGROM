from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr

from db.managers import BaseManager


class Base(DeclarativeBase):
    __abstract__ = True
    _manager_cls: BaseManager = BaseManager
    _manager = None

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    @classmethod
    def manager(cls, session) -> BaseManager:
        if cls._manager is None:
            cls._manager = cls._manager_cls(cls, session)
        return cls._manager
