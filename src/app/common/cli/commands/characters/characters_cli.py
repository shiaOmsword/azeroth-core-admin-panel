import typer
from typing import Annotated
import asyncio
from app.common.bootstrap.use_cases.characters import CHARACTER_USE_CASES_GROUP
from app.common.bootstrap.di import BuildDi
from app.common.ui.console import console

app = typer.Typer(help="Команды для работы с персонажами")


async def async_list_characters(page:int = 0) -> None:
    container = BuildDi().build()
    list_use_case = container.resolve(CHARACTER_USE_CASES_GROUP.get("list"))
    result = await list_use_case.execute(page=page)
    console.print(result)
    
async def async_get_character_by_account_id(account_id:int) -> None:
    container = BuildDi().build()
    use_case = container.resolve(CHARACTER_USE_CASES_GROUP.get("get_by_account_id"))
    result = await use_case.execute(account_id)
    console.print(result)
    
async def async_get_character_by_name(name:str) -> None:
    container = BuildDi().build()
    use_case = container.resolve(CHARACTER_USE_CASES_GROUP.get("get_by_character_name"))
    result = await use_case.execute(name)
    console.print(result)    
    
async def set_talents(char_id:int, value:int) -> None:
    container = BuildDi().build()
    use_case = container.resolve(CHARACTER_USE_CASES_GROUP.get("set_extra_talent_points"))
    result = await use_case.execute(id=char_id,value=value)
    console.print(result)    
    
@app.command("list")
def list_characters(
    page:Annotated[int, "--page", typer.Option(help="Номер страницы для отображения")] = 0,
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

@app.command("talents")
def runner(
    id:Annotated[int, "--id", typer.Argument(help="guid character")],
    value:Annotated[int, "--value", typer.Argument(help="how many talents")],
) -> None:
    asyncio.run(
        set_talents(char_id=id, value=value)
    )