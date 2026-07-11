import logging
from app.modules.acore_adapter.common.interface.gateways import WorldCommandGateway
logger = logging.getLogger(__name__)
from app.modules.acore_adapter.infrastructure.remote.dto import (
    WorldCommandResult,
)

class CheckSoapConnectionUseCase:
    def __init__(
        self,
        soap_client: WorldCommandGateway,
    ) -> None:
        self._soap_client = soap_client

    async def execute(self) -> WorldCommandResult:
        return await self._soap_client.execute(
            "server info"
        )