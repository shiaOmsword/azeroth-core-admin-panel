from typing import TypeVar, Type
from app.modules.acore_adapter.application.remote.use_cases.execute_command import ExecuteWorldCommandUseCase
from app.modules.acore_adapter.application.remote.use_cases.check import CheckSoapConnectionUseCase
from app.modules.acore_adapter.application.remote.use_cases.characters.set_level import SetCharacterLevelUseCase
from app.modules.acore_adapter.application.world.items.use_cases.get_item_template import GetItemTemplateUseCase
T = TypeVar("T")

WORLD_USE_CASES_GROUP:dict[str, Type[T]] = {
    "execute": ExecuteWorldCommandUseCase,
    "check": CheckSoapConnectionUseCase,
    "level": SetCharacterLevelUseCase,
    "item_template": GetItemTemplateUseCase,
}

__all__ = [
    "ExecuteWorldCommandUseCase",
    "CheckSoapConnectionUseCase",
    "WORLD_USE_CASES_GROUP",
]
