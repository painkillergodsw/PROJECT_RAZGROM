from pydantic import BaseModel
from db.managers import BaseManager


class ProjectManager(BaseManager):

    @BaseManager.commit_or_rollback(refresh=True)
    async def add(self, instance: BaseModel | dict):
        return await super().add(instance)


class MainDomainManager(BaseManager):

    @BaseManager.commit_or_rollback()
    async def add(self, instance: BaseModel | dict):
        return await super().add(instance)

    @BaseManager.commit_or_rollback()
    async def bulk_add(self, instances: list[BaseModel] | list[dict]):
        return await super().bulk_add(instances)
