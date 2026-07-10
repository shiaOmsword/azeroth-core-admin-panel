import asyncio
import typer
import punq
from app.modules.acore_adapter.infrastructure.remote.factory import build_acore_soap_client
from app.modules.acore_adapter.application.remote.use_cases.check import CheckSoapConnectionUseCase
from app.common.bootstrap.di import BuildDi
from app.common.ui.console import console

app = typer.Typer(name="worldserver")

@app.command("command")
def execute_command(command: str) -> None:
    async def runner() -> None:
        container = BuildDi().build()
        use_case = container.resolve(CheckSoapConnectionUseCase)
        result = await use_case.execute(command)
        console.print(result.raw_response)

    asyncio.run(runner())    
    
@app.command("info")
def server_info() -> None:
    async def runner() -> None:
        container = BuildDi().build()
        use_case = container.resolve(CheckSoapConnectionUseCase)
        result = await use_case.execute()
        console.print(result.raw_response)

    asyncio.run(runner())    