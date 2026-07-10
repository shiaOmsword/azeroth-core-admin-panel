import typer
import punq
from typing import Annotated
import asyncio
from app.modules.acore_adapter.application.auth.realmlist.use_cases.get_all import ListRealmlistsUseCase
from app.modules.acore_adapter.application.auth.realmlist.use_cases.set_addres import SetRealmlistAddresUseCase

from app.common.bootstrap.di import BuildDi
from app.common.ui.console import console

app = typer.Typer(help="Команды для работы с realmlist")


async def async_list_realms(page:int = 0) -> None:
    container = BuildDi().build()
    use_case = container.resolve(ListRealmlistsUseCase)
    result = await use_case.execute(page=page)
    console.print(result)
    
async def async_set_realmlist_addres(id:int, addres:str) -> None:
    container = BuildDi().build()
    use_case = container.resolve(SetRealmlistAddresUseCase)
    result = await use_case.execute(id=id, addres=addres)
    console.print(result)
    

@app.command("list")
def list_realms(
    page:Annotated[int, "--page", typer.Option(help="Номер страницы для отображения")] = 0,
) -> None:
    asyncio.run(
        async_list_realms(
            page=page
        )
    )
    
@app.command("set-addres")
def get_by_character_id(
    addres:Annotated[str, "--addres", typer.Argument(help="локальный адрес который будем ставить")],
    id:Annotated[int, "--id", typer.Argument(help="ID realmlist,обычно = 1")] = 1,
)-> None:
    asyncio.run(
        async_set_realmlist_addres(
            id=id,
            addres=addres,
        )
    )  
    
    