import json
from pathlib import Path
from typing import Any

from .enchantments import EnchantmentSlot
class EnchantmentCatalog:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._enchantments = self._load()

    def _load(self) -> dict[str, dict[str, Any]]:
        with self._path.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        enchantments = payload.get("enchantments")

        if not isinstance(enchantments, dict):
            raise ValueError(
                f"Invalid enchantment catalog: {self._path}"
            )

        return enchantments

    def get(self, enchantment_id: int) -> dict[str, Any] | None:
        return self._enchantments.get(str(enchantment_id))
    
    
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ItemEnchantmentInfo:
    slot: EnchantmentSlot
    enchantment_id: int
    duration: int
    charges: int
    name: str
    effect_summary: str
    effects: list[dict[str, Any]]    