from functools import wraps

from pydantic import BaseModel
from sqlalchemy import select, Select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from logger import logger as l
from sqlalchemy.orm import selectinload


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

    async def bulk_add(self, instances: list[BaseModel] | list[dict]):
        values_list = [
            (
                instance.model_dump(exclude_unset=True)
                if isinstance(instance, BaseModel)
                else instance
            )
            for instance in instances
        ]
        query = insert(self.model_cls).values(values_list)
        instances = await self._session.execute(query)
        l.info(f"Добавление списка {self.model_cls.__name__} {values_list}")
        l.info(f"querry: {query}")

        return instances

    async def get_one_or_none(
        self,
        filters: BaseModel | dict,
        selectinload_attr: str | None = None,
        selectinload_f: bool = False,
    ):
        filter_dict = (
            filters.model_dump(exclude_unset=True)
            if isinstance(filters, BaseModel)
            else filters
        )

        try:
            query = select(self.model_cls).filter_by(**filter_dict)
            if selectinload_f:
                query = query.options(
                    selectinload(getattr(self.model_cls, selectinload_attr))
                )

            result = await self._session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            l.error(f"Ошибка при поиске записи по фильтрам {filter_dict}: {e}")
            raise

    async def get_list(
        self,
        filters: BaseModel | dict,
        selectinload_attr: str | None = None,
        selectinload_f: bool = False,
    ):
        filter_dict = (
            filters.model_dump(exclude_unset=True)
            if isinstance(filters, BaseModel)
            else filters
        )

        try:
            query = select(self.model_cls).filter_by(**filter_dict)
            if selectinload_f:
                query = query.options(
                    selectinload(getattr(self.model_cls, selectinload_attr))
                )
            result = await self._session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            l.error(f"Ошибка при поиске записи по фильтрам {filter_dict}: {e}")
            raise
