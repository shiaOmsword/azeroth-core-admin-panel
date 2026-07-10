import typer
import punq
from typing import Annotated
import asyncio
from app.modules.acore_adapter.application.characters.use_cases.get_all import ListCharactersUseCase
from app.modules.acore_adapter.application.characters.use_cases.get_by_id import GetCharacterByIdUseCase
from app.modules.acore_adapter.application.characters.use_cases.get_by_account_id import GetCharacterByAccountIdUseCase
from app.modules.acore_adapter.application.characters.use_cases.get_by_name import GetCharacterByCharacterNameUseCase

from app.common.bootstrap.di import BuildDi
from app.common.ui.console import console

app = typer.Typer(help="Команды для работы с персонажами")


async def async_list_characters(page:int = 0) -> None:
    container = BuildDi().build()
    list_use_case = container.resolve(ListCharactersUseCase)
    result = await list_use_case.execute(page=page)
    console.print(result)
    
async def async_get_character_by_account_id(account_id:int) -> None:
    container = BuildDi().build()
    use_case = container.resolve(GetCharacterByAccountIdUseCase)
    result = await use_case.execute(account_id)
    console.print(result)
    
async def async_get_character_by_name(name:str) -> None:
    container = BuildDi().build()
    use_case = container.resolve(GetCharacterByCharacterNameUseCase)
    result = await use_case.execute(name)
    console.print(result)    
    
@app.command("list")
def list_characters(
    page:Annotated[int | None, "--page", typer.Option(help="Номер страницы для отображения")] = 0,
) -> None:
    asyncio.run(
        async_list_characters(
            page=page
        )
    )
    
@app.command("get")
def get_by_character_id(
    account_id:Annotated[int, "--id", typer.Argument(help="ID аккуанта пользователя")],
)-> None:
    asyncio.run(
        async_get_character_by_account_id(
            account_id=account_id
        )
    )  
    
@app.command("name")
def get_by_character_name(
    name:Annotated[str, "--name", typer.Argument(help="Имя персонажа")],
)-> None:
    asyncio.run(
        async_get_character_by_name(
            name=name
        )
    )      
    