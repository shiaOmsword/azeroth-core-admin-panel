from typing import TypeVar, Type
from app.modules.acore_adapter.application.remote.use_cases.execute_command import ExecuteWorldCommandUseCase
from app.modules.acore_adapter.application.remote.use_cases.check import CheckSoapConnectionUseCase

T = TypeVar("T")

WORLD_USE_CASES_GROUP:dict[str, Type[T]] = {
    "execute": ExecuteWorldCommandUseCase,
    "check": CheckSoapConnectionUseCase,
}

__all__ = [
    "ExecuteWorldCommandUseCase",
    "CheckSoapConnectionUseCase",
    "WORLD_USE_CASES_GROUP",
]
