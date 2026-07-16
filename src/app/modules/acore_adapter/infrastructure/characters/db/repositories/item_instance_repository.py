from typing import Protocol

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.acore_adapter.domain.acore_characters.item_instances.item_instance import (
    ItemInstance,
)
from app.modules.acore_adapter.infrastructure.characters.db.mappers.item_instance_mapper import (
    ItemInstanceMapper,
)
from app.modules.acore_adapter.infrastructure.characters.db.models.item_instance_model import (
    ItemInstanceModel,
)


class ItemInstanceRepositoryProtocol(Protocol):
    async def get(self, instance_guid: int) -> ItemInstance | None:
        ...

    async def update_enchantments(
        self,
        item_instance_id: int,
        enchantments: str,
    ) -> None:
        ...


class ItemInstanceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, instance_guid: int) -> ItemInstance | None:
        stmt = select(ItemInstanceModel).where(
            ItemInstanceModel.guid == instance_guid
        )
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        if instance is None:
            return None
        return ItemInstanceMapper.map_orm_to_dto(instance)

    async def update_enchantments(
        self,
        item_instance_id: int,
        enchantments: str,
    ) -> None:
        stmt = (
            update(ItemInstanceModel)
            .where(ItemInstanceModel.guid == item_instance_id)
            .values(enchantments=enchantments)
        )
        await self.session.execute(stmt)
