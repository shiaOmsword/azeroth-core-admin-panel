import punq
from typing import Type, TypeVar
from app.modules.acore_adapter.application.tests.use_cases.di_checker import TestDiRegister
from app.common.bootstrap.use_cases.characters import CHARACTER_USE_CASES_GROUP
from app.common.bootstrap.use_cases.auth import AUTH_USECASES_GROUP
from app.common.bootstrap.use_cases.world import WORLD_USE_CASES_GROUP

T = TypeVar("T")
class RegisterUseCases:
    def __init__(self, container: punq.Container):
        self.container = container
        
    def _cycle_usecases(self, group:list[Type[T]]) -> None:
        for item in group:
            self.container.register(item)

    def register(self) -> None:
        self._cycle_usecases(CHARACTER_USE_CASES_GROUP.values())
        self._cycle_usecases(AUTH_USECASES_GROUP.values())
        self._cycle_usecases(WORLD_USE_CASES_GROUP.values())
        
        self.container.register(TestDiRegister)

    
    
    