import punq
from app.modules.acore_adapter.application.tests.use_cases.di_checker import TestDiRegister
from app.modules.acore_adapter.application.characters.use_cases.get_by_id import GetCharacterByIdUseCase
from app.modules.acore_adapter.application.characters.use_cases.get_all import ListCharactersUseCase
from app.modules.acore_adapter.application.characters.use_cases.get_by_account_id import GetCharacterByAccountIdUseCase
from app.modules.acore_adapter.application.characters.use_cases.get_by_name import GetCharacterByCharacterNameUseCase
from app.modules.acore_adapter.application.remote.use_cases.check import CheckSoapConnectionUseCase
class RegisterUseCases:
    def __init__(self, container: punq.Container):
        self.container = container

    def register(self) -> None:
        self.container.register(CheckSoapConnectionUseCase)
        self.container.register(TestDiRegister)
        self.container.register(GetCharacterByIdUseCase)
        self.container.register(ListCharactersUseCase)
        self.container.register(GetCharacterByAccountIdUseCase)
        self.container.register(GetCharacterByCharacterNameUseCase)
        

    
    
    