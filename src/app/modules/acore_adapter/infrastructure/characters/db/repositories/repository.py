# app/modules/characters/infrastructure/db/repositories.py

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.acore_adapter.infrastructure.characters.db.models.character_model import CharacterModel
from app.modules.acore_adapter.domain.acore_characters.entity.character import CharacterDTO, CharactersDTO
from app.modules.acore_adapter.infrastructure.characters.db.mapper import CharacterMapper

from app.common.errors.base_exceptions import NotFoundError

class CharacterRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, limit: int = 50, offset: int = 0) -> CharactersDTO:
        stmt = (
            select(CharacterModel)
            .limit(limit)
            .offset(offset)
            .order_by(CharacterModel.guid)
        )
        
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        characters = [CharacterMapper.map_to_dto(model) for model in models]
        return CharactersDTO.from_characters(characters)
    
    async def get_by_id(self, id:int) -> CharacterModel | None:
        stmt = select(CharacterModel).where(CharacterModel.guid == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_account_id(self, account_id:int) -> CharactersDTO:
        stmt = (
            select(CharacterModel)
            .where(CharacterModel.account == account_id)
        )

        result = await self.session.execute(stmt)
        models = result.scalars().all()
        characters = [CharacterMapper.map_to_dto(model) for model in models]
        return CharactersDTO.from_characters(characters)  

    async def get_by_guid(self, guid: int) -> CharacterDTO|None:
        stmt = (
            select(CharacterModel)
            .where(CharacterModel.guid == guid)
        )

        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return CharacterMapper.map_to_dto(model)

    async def get_by_name(self, name: str) -> CharacterDTO | None:
        stmt = (
            select(CharacterModel)
            .where(CharacterModel.name == name)
        )

        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            return CharacterMapper.map_to_dto(model)

    # TODO need to refactor method and add use_case
    async def set_money(self, guid: int, money: int) -> None:
        stmt = (
            update(CharacterModel)
            .where(CharacterModel.guid == guid)
            .values(money=money)
        )

        await self.session.execute(stmt)
        
    async def set_extra_talent(self, guid:int, value:int) -> CharacterDTO | str:
        char = await self.get_by_id(guid)
        if char is None:
            return NotFoundError()
        
        char.extraBonusTalentCount = value
        await self.session.flush()
        await self.session.refresh(char)
        return CharacterMapper.map_to_dto(char)
    
    async def update(self, char:CharacterDTO) -> CharacterDTO | str:
        char = await self.get_by_id(char.guid)
        if char is None:
            return NotFoundError()
        stmt = select(CharacterModel).where(CharacterModel.guid == char.guid)
        result = await self.session.execute(stmt)
        orm = result.scalar_one_or_none()
        
        if orm is None:
            raise NotFoundError
        
        CharacterMapper.update_orm(orm=orm,entity=char)
        
                