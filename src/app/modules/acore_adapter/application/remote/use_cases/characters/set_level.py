from app.modules.acore_adapter.application.remote.commands import (
    WorldCommands,
)
from app.modules.acore_adapter.application.remote.gateways import (
    WorldCommandGateway,
)
from app.modules.acore_adapter.infrastructure.remote.dto import (
    WorldCommandResult,
)


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
            raise ValueError("Character name cannot be empty")

        if not 1 <= level <= 80:
            raise ValueError(
                "Character level must be between 1 and 80"
            )

        command = WorldCommands.set_character_level(
            character_name=character_name,
            level=level,
        )

        return await self._gateway.execute(command)