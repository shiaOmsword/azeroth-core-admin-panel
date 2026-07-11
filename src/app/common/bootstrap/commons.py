import punq
from app.config.settings import settings, Settings
from app.common.infrastructure.db.session import (
    auth_session_factory,
    world_session_factory,
    characters_session_factory,
)
from app.common.infrastructure.db.providers import(
    AuthSessionProvider,
    CharactersSessionProvider,
    WorldSessionProvider,
)
from app.common.infrastructure.db.uow import (
    UnitsOfWork, CharactersUnitOfWorkFactory, RealmlistsUnitOfWorkFactory
)
from app.common.protocols.uows import UowsProtocol

from app.modules.acore_adapter.infrastructure.remote.factory import build_acore_soap_client
from app.modules.acore_adapter.common.gateways import WorldCommandGateway
class RegisterCommons:
    def __init__(self, container: punq.Container):
        self.container = container

    def register(self) -> None:
        self.container.register(Settings, instance=settings)

        self.container.register(
            AuthSessionProvider,
            instance=AuthSessionProvider(auth_session_factory),
        )

        self.container.register(
            CharactersSessionProvider,
            instance=CharactersSessionProvider(characters_session_factory),
        )

        self.container.register(
            WorldSessionProvider,
            instance=WorldSessionProvider(world_session_factory),
        )
        
        self.container.register(CharactersUnitOfWorkFactory)
        self.container.register(RealmlistsUnitOfWorkFactory)
        self.container.register(
            UowsProtocol,
            UnitsOfWork,
        )
        
        soap_client = build_acore_soap_client()
        self.container.register(WorldCommandGateway, instance=soap_client)