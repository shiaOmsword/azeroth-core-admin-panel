from typing import Protocol

from app.modules.acore_adapter.infrastructure.remote.dto import (
    WorldCommandResult,
)


class WorldCommandGateway(Protocol):
    async def execute(
        self,
        command: str,
    ) -> WorldCommandResult:
        ...