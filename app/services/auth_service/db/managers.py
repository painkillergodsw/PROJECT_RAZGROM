from functools import wraps

from pydantic import BaseModel
from sqlalchemy import select, Select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from logger import logger as l


class BaseManager:

    def __init__(self, model_cls, session):
        self.model_cls = model_cls
        self._session: AsyncSession = session

    @staticmethod
    def commit_or_rollback(refresh=False):
        def decorator(method):
            @wraps(method)
            async def wrapper(self, *args, **kwargs):
                try:
                    result = await method(self, *args, **kwargs)
                    await self._session.commit()
                    l.info("Выполнен коммит")
                    if refresh:
                        await self._session.refresh(result)
                    return result
                except Exception:
                    await self._session.rollback()
                    l.info("Выполнен откат")
                    raise

            return wrapper

        return decorator

    async def add(self, instance: BaseModel | dict):
        values = (
            instance.model_dump(exclude_unset=True)
            if isinstance(instance, BaseModel)
            else instance
        )

        l.info(f"Добавление {self.model_cls.__name__} {values}")
        instance = self.model_cls(**values)
        self._session.add(instance)
        return instance

    async def get_one_or_none(self, filters: BaseModel | dict):
        filter_dict = (
            filters.model_dump(exclude_unset=True)
            if isinstance(filters, BaseModel)
            else filters
        )

        try:
            query = select(self.model_cls).filter_by(**filter_dict)
            result = await self._session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            l.error(f"Ошибка при поиске записи по фильтрам {filter_dict}: {e}")
            raise
