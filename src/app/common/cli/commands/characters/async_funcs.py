from collections.abc import Callable
from typing import TypeVar, Type, Any
from app.common.bootstrap.use_cases.characters import CHARACTER_USE_CASES_GROUP
from app.common.bootstrap.di import BuildDi
from app.common.ui.console import console

T = TypeVar("T")
class AsyncFuncFactory:
    def __init__(self, use_case:Type[T]):
        self.container = BuildDi().build()
        self.use_case = self.container.resolve(use_case)
        
    async def result(self, *args, **kwargs) -> None:
        response = await self.use_case.execute(*args,**kwargs)
        console.print(response)
        
async def async_list_characters(page:int = 0) -> None:
    func = AsyncFuncFactory(CHARACTER_USE_CASES_GROUP.get("list"))
    await func.result(page=page)
    
async def async_get_character_by_account_id(account_id:int) -> None:
    func = AsyncFuncFactory(CHARACTER_USE_CASES_GROUP.get("get_by_account_id"))
    await func.result(account_id=account_id)
    
async def async_get_character_by_name(name:str) -> None:
    func = AsyncFuncFactory(CHARACTER_USE_CASES_GROUP.get("get_by_character_name"))
    await func.result(name=name)
    
async def set_talents(char_id:int, value:int) -> None:
    func = AsyncFuncFactory(CHARACTER_USE_CASES_GROUP.get("set_extra_talent_points"))
    await func.result(char_id=char_id, value=value)
    
async def change_name(char_id:int, value:str) -> None:
    func = AsyncFuncFactory(CHARACTER_USE_CASES_GROUP.get("change_name"))
    await func.result(char_id=char_id, value=value)
    
ASYNC_FUNCS_CHARACTERS_GROUP = {
    "list":async_list_characters,
    "get_by_account_id":async_get_character_by_account_id,
    "get_by_character_name":async_get_character_by_name,
    "set_extra_talent_points":set_talents,
    "change_name":change_name,
}