import punq

from app.modules.acore_adapter.application.tests.use_cases.di_checker import TestDiRegister

from app.modules.acore_adapter.application.characters.use_cases.get_by_id import GetCharacterByIdUseCase
from app.modules.acore_adapter.application.characters.use_cases.get_all import ListCharactersUseCase
from app.modules.acore_adapter.application.characters.use_cases.get_by_account_id import GetCharacterByAccountIdUseCase
from app.modules.acore_adapter.application.characters.use_cases.get_by_name import GetCharacterByCharacterNameUseCase
from app.modules.acore_adapter.application.characters.use_cases.set_extra_talent_points import SetCharacterExtraTalentPointsUseCase

from app.modules.acore_adapter.application.remote.use_cases.execute_command import ExecuteWorldCommandUseCase
from app.modules.acore_adapter.application.remote.use_cases.check import CheckSoapConnectionUseCase
from app.modules.acore_adapter.application.remote.use_cases.characters.set_level import SetCharacterLevelUseCase


from app.modules.acore_adapter.application.auth.realmlist.use_cases.get_all import ListRealmlistsUseCase
from app.modules.acore_adapter.application.auth.realmlist.use_cases.set_addres import SetRealmlistAddresUseCase

class RegisterUseCases:
    def __init__(self, container: punq.Container):
        self.container = container

    def register(self) -> None:
        self.container.register(CheckSoapConnectionUseCase)
        self.container.register(ExecuteWorldCommandUseCase)
        
        self.container.register(TestDiRegister)
        
        self.container.register(GetCharacterByIdUseCase)
        self.container.register(ListCharactersUseCase)
        self.container.register(GetCharacterByAccountIdUseCase)
        self.container.register(GetCharacterByCharacterNameUseCase)
        self.container.register(SetCharacterExtraTalentPointsUseCase)
        
        
        #character world commands
        self.container.register(SetCharacterLevelUseCase)


        self.container.register(ListRealmlistsUseCase)
        self.container.register(SetRealmlistAddresUseCase)
    
    
    