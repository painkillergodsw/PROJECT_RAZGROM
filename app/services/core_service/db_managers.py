from pydantic import BaseModel
from db.managers import BaseManager


class ProjectManager(BaseManager):

    @BaseManager.commit_or_rollback(refresh=True)
    async def add(self, instance: BaseModel | dict):
        return await super().add(instance)

    async def get_list(
        self,
        filters: BaseModel | dict,
        selectinload_attr: str | None = None,
        selectinload_f: bool = False,
    ):
        return await super().get_list(filters, "main_domains", True)

    async def get_one_or_none(
        self,
        filters: BaseModel | dict,
        selectinload_attr: str | None = None,
        selectinload_f: bool = False,
    ):
        return await super().get_one_or_none(filters, "main_domains", True)


class MainDomainManager(BaseManager):

    @BaseManager.commit_or_rollback()
    async def add(self, instance: BaseModel | dict):
        return await super().add(instance)

    @BaseManager.commit_or_rollback()
    async def bulk_add(self, instances: list[BaseModel] | list[dict]):
        return await super().bulk_add(instances)
