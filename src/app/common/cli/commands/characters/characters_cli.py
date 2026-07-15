import typer
import asyncio
from app.common.cli.commands.characters.async_funcs import ASYNC_FUNCS_CHARACTERS_GROUP
from .annotations import Page, AccountId, CharacterName, CharacterId, Value, StrValue, ItemInstanceId
app = typer.Typer(help="Команды для работы с персонажами")


@app.command("inventory")
def execute_command(
    character_id: AccountId
) -> None:
    asyncio.run(ASYNC_FUNCS_CHARACTERS_GROUP["inventory"](
        character_id=character_id
    ))
    
@app.command("raw-inventory")
def execute_command(
    character_id: AccountId
) -> None:
    asyncio.run(ASYNC_FUNCS_CHARACTERS_GROUP["character_inventory"](
        character_id=character_id
    ))    
    
    
@app.command("update-item")
def execute_command(
    item_instance_id: ItemInstanceId
) -> None:
    asyncio.run(ASYNC_FUNCS_CHARACTERS_GROUP["update_item"](
        item_instance_id=item_instance_id
    ))        

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