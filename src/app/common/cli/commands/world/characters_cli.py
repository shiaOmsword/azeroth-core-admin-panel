import asyncio
import typer
from typing import Annotated
from app.common.bootstrap.di import BuildDi
from app.common.ui.console import console
from app.modules.acore_adapter.application.remote.use_cases.characters.set_level import SetCharacterLevelUseCase

app = typer.Typer(name="characters")

@app.command("level")
def execute_command(
    character_name: Annotated[str, "--name", typer.Argument(help="Имя персонажа")], 
    level:Annotated[int, "--level", typer.Argument(help="Уровень персонажа")], 
) -> None:
    async def runner() -> None:
        container = BuildDi().build()
        use_case = container.resolve(SetCharacterLevelUseCase)

        result = await use_case.execute(character_name=character_name,level=level)
        console.print(result.raw_response)

    asyncio.run(runner())
    