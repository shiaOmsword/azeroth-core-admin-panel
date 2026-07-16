from collections.abc import Callable
from typing import TypeVar, Type, Any, Protocol
from punq import Container
from app.common.bootstrap.use_cases.characters import CHARACTER_USE_CASES_GROUP
from app.common.bootstrap.di import BuildDi
from app.common.ui.console import console
from app.modules.acore_adapter.application.acore_characters.characters.dto import CharacterReadDTO

class ExecutableUseCase(Protocol):
    async def execute(self, *args:Any, **kwargs:Any)->Any:
        ...
        
TUseCase = TypeVar("TUseCase", bound=ExecutableUseCase)
class AsyncUseCaseRunner:
    def __init__(self, container: Container) -> None:
        self._container = container
    
    async def run(
        self,
        use_case_type:type[TUseCase],
        *args, 
        **kwargs
    ) -> Any:
        use_case = self._container.resolve(use_case_type)
        response = await use_case.execute(*args,**kwargs)
        console.print(response)
        return response
container = BuildDi().build()
runner = AsyncUseCaseRunner(container=container)

async def async_list_characters(page:int = 0) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["list"],
        page=page
    )
async def async_get_character_by_account_id(account_id:int) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["get_by_account_id"],
        account_id=account_id
        )
async def async_get_character_by_name(name:str) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["get_by_character_name"],
        name=name
    )

async def set_talents(char_id:int, value:int) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["set_extra_talent_points"],
        character_id=char_id,
        value=value
    )
    
async def change_name(char_id:int, value:str) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["change_name"],
        char_id=char_id,
        value=value
    )
    
async def get_raw_character_inventory(character_id:int) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["character_inventory"],
        character_id=character_id
    )
    
    
async def update_instance_item(item_instance_id:int) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["update_item"],
        item_instance_id=item_instance_id
    )    
        
async def get_character_inventory(character_id:int) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["inventory_o"],
        character_id=character_id
    )

ASYNC_FUNCS_CHARACTERS_GROUP = {
    "list":async_list_characters,
    "get_by_account_id":async_get_character_by_account_id,
    "get_by_character_name":async_get_character_by_name,
    "set_extra_talent_points":set_talents,
    "change_name":change_name,
    "inventory":get_character_inventory,
    "character_inventory":get_raw_character_inventory,
    "update_item":update_instance_item,
}