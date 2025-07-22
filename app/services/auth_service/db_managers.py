from pydantic import BaseModel

from db.managers import BaseManager


class UserManager(BaseManager):

    @BaseManager.commit_or_rollback(refresh=True)
    def add(self, instance: BaseModel | dict):
        return super().add(instance)


class RoleManager(BaseManager):

    @BaseManager.commit_or_rollback()
    def add(self, instance: BaseModel | dict):
        return super().add(instance)


class JWTBlackListManager(BaseManager):

    @BaseManager.commit_or_rollback()
    def add(self, instance: BaseModel | dict):
        return super().add(instance)
