import logging
from app.modules.acore_adapter.common.interface.gateways import WorldCommandGateway
logger = logging.getLogger(__name__)

class ExecuteWorldCommandUseCase:
    def __init__(
        self, 
        client:WorldCommandGateway
    ):
        self.client = client
        
    async def execute(
        self,
        command:str,
    ):
        return await self.client.execute(command)