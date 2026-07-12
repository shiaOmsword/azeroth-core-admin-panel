import typer
import asyncio
from app.common.cli.commands.characters.async_funcs import ASYNC_FUNCS_CHARACTERS_GROUP
from .annotations import Page, AccountId, CharacterName, CharacterId, Value, StrValue
app = typer.Typer(help="Команды для работы с персонажами")

@app.command("list")
def list_characters(
    page:Page = 0,
) -> None:
    asyncio.run(
        ASYNC_FUNCS_CHARACTERS_GROUP["list"](
            page=page
        )
    )
    
@app.command("get")
def get_by_account_id(
    account_id: AccountId,
)-> None:
    asyncio.run(
        ASYNC_FUNCS_CHARACTERS_GROUP["get_by_account_id"](
            account_id=account_id
        )
    )  
    
@app.command("name")
def get_by_character_name(
    name:CharacterName,
)-> None:
    asyncio.run(
        ASYNC_FUNCS_CHARACTERS_GROUP["get_by_character_name"](
            name=name
        )
    )      

@app.command("talents")
def runner(
    id:CharacterId,
    value:Value,
) -> None:
    asyncio.run(
        ASYNC_FUNCS_CHARACTERS_GROUP["set_extra_talent_points"](
            char_id=id, 
            value=value,
        )
    )
    
@app.command("change-name")
def runner(
    id:CharacterId,
    value:StrValue,
) -> None:
    asyncio.run(
        ASYNC_FUNCS_CHARACTERS_GROUP["change_name"](
            char_id=id, 
            value=value,
        )
    )    