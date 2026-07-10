import punq
from .commons import RegisterCommons
from .use_cases import RegisterUseCases

class BuildDi:
    def build(self) -> punq.Container:
        container = punq.Container()

        RegisterCommons(container).register()
        RegisterUseCases(container).register()

        return container
    
    
    