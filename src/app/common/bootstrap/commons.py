import punq
from pathlib import Path
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
    UnitsOfWork, CharactersUnitOfWorkFactory, AuthUnitOfWorkFactory, WorldUnitOfWorkFactory
)

from app.common.protocols.uows import UowsProtocol

from app.modules.acore_adapter.infrastructure.remote.factory import build_acore_soap_client
from app.modules.acore_adapter.common.interface.gateways import WorldCommandGateway
from app.modules.acore_adapter.infrastructure.characters.enchantments.json_enchantment_catalog import JsonEnchantmentCatalog
from app.modules.acore_adapter.application.acore_characters.item_instances.ports.enchantment_catalog import EnchantmentCatalog
from app.modules.acore_adapter.infrastructure.characters.enchantments.yaml_enchants_sets_reader import YamlSetsReader
from app.modules.acore_adapter.common.interface.repositories import SetsReader
from app.modules.acore_adapter.application.acore_characters.item_instances.services.item_enchantments_planner import (
    ItemEnchantmentsPlanner,
)
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
        self.container.register(AuthUnitOfWorkFactory)
        self.container.register(WorldUnitOfWorkFactory)
        self.container.register(
            UowsProtocol,
            UnitsOfWork,
        )
        
        soap_client = build_acore_soap_client()
        self.container.register(WorldCommandGateway, instance=soap_client)
        
        self.container.register(
            EnchantmentCatalog,
            instance=JsonEnchantmentCatalog(Path(settings.json_enchants_catalog)),
        )        
        
        self.container.register(
            SetsReader,
            instance=YamlSetsReader(settings.enchantments_set_catalog),
        )  
        self.container.register(
            ItemEnchantmentsPlanner,
            ItemEnchantmentsPlanner,
        )
