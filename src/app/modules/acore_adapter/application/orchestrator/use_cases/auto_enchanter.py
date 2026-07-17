from collections.abc import Sequence

from app.common.protocols.uows import UowsProtocol
from app.modules.acore_adapter.application.acore_characters.item_instances.dto.enchantments import (
    ItemEnchantmentsUpdate,
)
from app.modules.acore_adapter.application.acore_characters.item_instances.ports.enchantment_catalog import (
    EnchantmentCatalog,
)
from app.modules.acore_adapter.application.acore_characters.item_instances.services.item_enchantments_planner import (
    ItemEnchantmentsPlanner,
)
from app.modules.acore_adapter.application.orchestrator.dto.auto_enchantments import (
    AutoEnchantCharacterResult,
)
from app.modules.acore_adapter.common.constants.classes import (
    get_character_classes_name,
)
from app.modules.acore_adapter.common.interface.repositories import SetsReader
from app.modules.acore_adapter.domain.acore_characters.exceptions.errors import (
    CharacterNotFoundError,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.enchantments import (
    EnchantmentDefinition,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.errors import (
    CharacterOnlineError,
    EnchantmentNotFoundError,
    UnsupportedCharacterClassError,
)


class AutoEnchantCharacterItemsUseCase:
    """Enchant all equipped character items using the configured class set.

    Database interaction is intentionally bounded to one character SELECT, one
    equipped-items SELECT, one bulk UPDATE and one COMMIT.
    """

    def __init__(
        self,
        uow_factory: UowsProtocol,
        reader: SetsReader,
        enchantment_catalog: EnchantmentCatalog,
        planner: ItemEnchantmentsPlanner,
    ) -> None:
        self._uow_factory = uow_factory
        self._reader = reader
        self._enchantment_catalog = enchantment_catalog
        self._planner = planner

    async def execute(
        self,
        character_id: int,
        *,
        overwrite: bool = False,
        dry_run: bool = False,
    ) -> AutoEnchantCharacterResult:
        async with self._uow_factory.characters_uow() as uow:
            character = await uow.characters.get_by_guid(character_id)
            if character is None:
                raise CharacterNotFoundError(
                    f"Character {character_id} was not found"
                )

            if bool(character.online):
                raise CharacterOnlineError(
                    f"Character {character.name} is online; item modification is unsafe"
                )

            character_class = get_character_classes_name(
                character.character_class
            )
            if character_class == "undefined":
                raise UnsupportedCharacterClassError(
                    f"Character class ID {character.character_class} is not supported"
                )

            requested_ids = tuple(
                self._reader.get_enchant_set(character_class)
            )
            definitions = self._resolve_definitions(requested_ids)

            equipped_items = (
                await uow.character_inventory.get_equipped_items_for_enchanting(
                    character_guid=character.guid,
                )
            )

            plans = tuple(
                self._planner.plan(
                    item=item,
                    enchantments_to_apply=definitions,
                    overwrite=overwrite,
                )
                for item in equipped_items
            )

            updates = tuple(
                ItemEnchantmentsUpdate(
                    item_instance_id=plan.item_instance_id,
                    enchantments=plan.new_enchantments,
                )
                for plan in plans
                if plan.changed
            )

            if not dry_run and updates:
                await uow.item_instance.update_enchantments_many(updates)
                await uow.commit()

            return AutoEnchantCharacterResult(
                character_guid=character.guid,
                character_name=character.name,
                character_class=character_class,
                requested_enchantment_ids=requested_ids,
                items=plans,
                updated_item_count=len(updates),
                skipped_enchantment_count=sum(
                    len(plan.skipped_enchantment_ids)
                    for plan in plans
                ),
                persisted=not dry_run and bool(updates),
            )

    def _resolve_definitions(
        self,
        enchantment_ids: Sequence[int],
    ) -> tuple[EnchantmentDefinition, ...]:
        definitions_by_id: dict[int, EnchantmentDefinition] = {}
        unknown_ids: list[int] = []

        # Resolve every unique ID only once. Duplicate IDs in a YAML set are
        # still preserved when the final ordered tuple is built below.
        for enchantment_id in dict.fromkeys(enchantment_ids):
            definition = self._enchantment_catalog.get(enchantment_id)
            if definition is None:
                unknown_ids.append(enchantment_id)
                continue
            definitions_by_id[enchantment_id] = definition

        if unknown_ids:
            raise EnchantmentNotFoundError(
                "Enchantments were not found in the catalog: "
                + ", ".join(str(value) for value in unknown_ids)
            )

        return tuple(
            definitions_by_id[enchantment_id]
            for enchantment_id in enchantment_ids
        )
