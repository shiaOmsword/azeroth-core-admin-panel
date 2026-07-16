from pathlib import Path
from typing import Any

import yaml

from app.modules.acore_adapter.domain.acore_characters.item_instances.errors import (
    EnchantSetConfigurationError,
    EnchantSetNotFoundError,
)


class YamlSetsReader:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._sets = self._load()

    def _load(self) -> dict[str, tuple[int, ...]]:
        with self._path.open("r", encoding="utf-8") as file:
            payload: Any = yaml.safe_load(file)

        if not isinstance(payload, dict):
            raise EnchantSetConfigurationError(
                f"Enchantments config {self._path} must contain a mapping"
            )

        raw_sets = payload.get("sets")
        if not isinstance(raw_sets, dict):
            raise EnchantSetConfigurationError(
                f"Enchantments config {self._path} must contain a 'sets' mapping"
            )

        parsed_sets: dict[str, tuple[int, ...]] = {}
        for class_name, raw_enchantment_ids in raw_sets.items():
            if not isinstance(class_name, str):
                raise EnchantSetConfigurationError(
                    "Every enchantment set name must be a string"
                )

            if not isinstance(raw_enchantment_ids, list):
                raise EnchantSetConfigurationError(
                    f"Enchantments set {class_name!r} must be a list"
                )

            if not raw_enchantment_ids:
                raise EnchantSetConfigurationError(
                    f"Enchantments set {class_name!r} cannot be empty"
                )

            if any(
                not isinstance(enchantment_id, int) or enchantment_id <= 0
                for enchantment_id in raw_enchantment_ids
            ):
                raise EnchantSetConfigurationError(
                    f"Enchantments set {class_name!r} must contain positive integers"
                )

            parsed_sets[class_name.strip().lower()] = tuple(raw_enchantment_ids)

        return parsed_sets

    def get_enchant_set(self, character_class: str) -> list[int]:
        normalized_class = character_class.strip().lower()
        enchantment_ids = self._sets.get(normalized_class)
        if enchantment_ids is None:
            raise EnchantSetNotFoundError(
                f"Enchantments set for character class {character_class!r} was not found"
            )
        return list(enchantment_ids)
