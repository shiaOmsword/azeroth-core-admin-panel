from typing import Protocol

from app.modules.acore_adapter.domain.acore_characters.item_instances.enchantments import (
    EnchantmentDefinition,
)


class EnchantmentCatalog(Protocol):
    """Application port for read-only enchantment definitions."""

    def get(self, enchantment_id: int) -> EnchantmentDefinition | None:
        ...
