import logging
from app.modules.acore_adapter.infrastructure.remote.soap_client import AcoreSoapClient
from app.common.ui.console import console

logger = logging.getLogger(__name__)

class CheckSoapConnectionUseCase:
    def __init__(self, client:AcoreSoapClient):
        self.client = client
        
    async def execute(self):
        result = await self.client.execute("server info")
        console.print("COMMAND:")
        console.print(result.command)
        console.print("RAW RESPONSE:")
        console.print(result.raw_response)