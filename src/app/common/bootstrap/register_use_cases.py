import punq
from typing import Type, TypeVar
from app.modules.acore_adapter.application.tests.use_cases.di_checker import TestDiRegister

from app.common.bootstrap.use_cases.characters import CHARACTER_USE_CASES_GROUP
from app.modules.acore_adapter.application.remote.use_cases.execute_command import ExecuteWorldCommandUseCase
from app.modules.acore_adapter.application.remote.use_cases.check import CheckSoapConnectionUseCase

from app.modules.acore_adapter.application.auth.realmlist.use_cases.get_all import ListRealmlistsUseCase
from app.modules.acore_adapter.application.auth.realmlist.use_cases.set_addres import SetRealmlistAddresUseCase

T = TypeVar("T")
class RegisterUseCases:
    def __init__(self, container: punq.Container):
        self.container = container
        
    def _cycle_usecases(self, group:list[Type[T]]) -> None:
        for item in group:
            self.container.register(item)

    def register(self) -> None:
        self._cycle_usecases(CHARACTER_USE_CASES_GROUP.values())

        self.container.register(CheckSoapConnectionUseCase)
        self.container.register(ExecuteWorldCommandUseCase)
        
        self.container.register(TestDiRegister)

        self.container.register(ListRealmlistsUseCase)
        self.container.register(SetRealmlistAddresUseCase)
    
    
    