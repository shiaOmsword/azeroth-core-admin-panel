import punq
from .commons import RegisterCommons
from app.common.bootstrap.register_use_cases import RegisterUseCases

class BuildDi:
    def build(self) -> punq.Container:
        container = punq.Container()

        RegisterCommons(container).register()
        RegisterUseCases(container).register()

        return container
    
    
    