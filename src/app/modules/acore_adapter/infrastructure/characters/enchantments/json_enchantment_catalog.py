import json
from pathlib import Path
from typing import Any

from app.modules.acore_adapter.domain.acore_characters.item_instances.enchantments import (
    EnchantmentDefinition,
)


class JsonEnchantmentCatalog:
    """JSON-backed implementation of EnchantmentCatalog."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._enchantments = self._load()

    def _load(self) -> dict[str, dict[str, Any]]:
        with self._path.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        enchantments = payload.get("enchantments")
        if not isinstance(enchantments, dict):
            raise ValueError(f"Invalid enchantment catalog: {self._path}")

        return enchantments

    def get(self, enchantment_id: int) -> EnchantmentDefinition | None:
        payload = self._enchantments.get(str(enchantment_id))
        if not isinstance(payload, dict):
            return None

        name = payload.get("name")
        effect_summary = payload.get("effect_summary")
        if not isinstance(name, str) or not isinstance(effect_summary, str):
            raise ValueError(
                f"Invalid enchantment {enchantment_id} in catalog {self._path}"
            )

        return EnchantmentDefinition(
            enchantment_id=enchantment_id,
            name=name,
            effect_summary=effect_summary,
        )
