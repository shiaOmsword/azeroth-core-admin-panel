from app.modules.acore_adapter.application.remote.commands import character
from app.modules.acore_adapter.common.gateways import (
    WorldCommandGateway,
)
from app.modules.acore_adapter.infrastructure.remote.dto import (
    WorldCommandResult,
)
from app.modules.acore_adapter.domain.characters.exceptions.errors import CharacterLevelRequiredError, CharacterNameEmptyError

class SetCharacterLevelUseCase:
    def __init__(
        self,
        gateway: WorldCommandGateway,
    ) -> None:
        self._gateway = gateway

    async def execute(
        self,
        character_name: str,
        level: int,
    ) -> WorldCommandResult:
        if not character_name.strip():
            raise CharacterNameEmptyError()

        if not 1 <= level <= 80:
            raise CharacterLevelRequiredError()

        command = character.CharacterWorldCommands().set_character_level(
            character_name=character_name,
            level=level,
        )

        return await self._gateway.execute(command)