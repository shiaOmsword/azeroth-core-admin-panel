import unittest
from dataclasses import dataclass

from app.modules.acore_adapter.application.acore_characters.item_instances.services.item_enchantments_planner import (
    ItemEnchantmentsPlanner,
)
from app.modules.acore_adapter.application.orchestrator.use_cases.auto_enchanter import (
    AutoEnchantCharacterItemsUseCase,
)
from app.modules.acore_adapter.domain.acore_characters.entity.character_inventory import (
    EnchantableEquipmentItem,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.enchantments import (
    EnchantmentDefinition,
    EnchantmentSlot,
    ItemEnchantments,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.errors import (
    EnchantmentNotFoundError,
)


@dataclass(slots=True)
class FakeCharacter:
    guid: int = 1305
    name: str = "Rogue"
    character_class: int = 4
    online: int = 0


class FakeCharacterRepository:
    def __init__(self, character: FakeCharacter | None) -> None:
        self.character = character
        self.calls = 0

    async def get_by_guid(self, guid: int) -> FakeCharacter | None:
        self.calls += 1
        if self.character is None or self.character.guid != guid:
            return None
        return self.character


class FakeInventoryRepository:
    def __init__(self, items: list[EnchantableEquipmentItem]) -> None:
        self.items = items
        self.calls = 0

    async def get_equipped_items_for_enchanting(
        self,
        character_guid: int,
    ) -> list[EnchantableEquipmentItem]:
        self.calls += 1
        return list(self.items)


class FakeItemInstanceRepository:
    def __init__(self) -> None:
        self.bulk_calls: list[tuple] = []

    async def update_enchantments_many(self, updates) -> None:
        self.bulk_calls.append(tuple(updates))


class FakeCharactersUnitOfWork:
    def __init__(
        self,
        character: FakeCharacter | None,
        items: list[EnchantableEquipmentItem],
    ) -> None:
        self.characters = FakeCharacterRepository(character)
        self.character_inventory = FakeInventoryRepository(items)
        self.item_instance = FakeItemInstanceRepository()
        self.commit_count = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback) -> None:
        return None

    async def commit(self) -> None:
        self.commit_count += 1


class FakeCharactersUnitOfWorkFactory:
    def __init__(self, uow: FakeCharactersUnitOfWork) -> None:
        self.uow = uow

    def __call__(self) -> FakeCharactersUnitOfWork:
        return self.uow


class FakeUnitsOfWork:
    def __init__(self, uow: FakeCharactersUnitOfWork) -> None:
        self.characters_uow = FakeCharactersUnitOfWorkFactory(uow)


class FakeSetsReader:
    def __init__(self, values: list[int]) -> None:
        self.values = values
        self.requested_classes: list[str] = []

    def get_enchant_set(self, character_class: str) -> list[int]:
        self.requested_classes.append(character_class)
        return list(self.values)


class FakeCatalog:
    def __init__(self, known_ids: set[int]) -> None:
        self.known_ids = known_ids
        self.calls: list[int] = []

    def get(self, enchantment_id: int) -> EnchantmentDefinition | None:
        self.calls.append(enchantment_id)
        if enchantment_id not in self.known_ids:
            return None
        return EnchantmentDefinition(
            enchantment_id=enchantment_id,
            name=f"Enchant {enchantment_id}",
            effect_summary=f"Effect {enchantment_id}",
        )


def enchantments_string(values_by_slot: dict[int, int] | None = None) -> str:
    values_by_slot = values_by_slot or {}
    values: list[str] = []
    for slot in range(12):
        values.extend((str(values_by_slot.get(slot, 0)), "0", "0"))
    return " ".join(values) + " "


def equipment_item(
    item_instance_id: int,
    equipment_slot: int,
    property_slots: dict[int, int] | None = None,
    random_property_id: int = 0,
) -> EnchantableEquipmentItem:
    return EnchantableEquipmentItem(
        item_instance_id=item_instance_id,
        item_template_id=12044 + equipment_slot,
        bag=0,
        equipment_slot=equipment_slot,
        enchantments=enchantments_string(property_slots),
        random_property_id=random_property_id,
    )


class AutoEnchantCharacterUseCaseTests(unittest.IsolatedAsyncioTestCase):
    def build_use_case(
        self,
        *,
        enchantment_ids: list[int],
        known_ids: set[int],
        items: list[EnchantableEquipmentItem],
    ):
        uow = FakeCharactersUnitOfWork(FakeCharacter(), items)
        reader = FakeSetsReader(enchantment_ids)
        catalog = FakeCatalog(known_ids)
        use_case = AutoEnchantCharacterItemsUseCase(
            uow_factory=FakeUnitsOfWork(uow),
            reader=reader,
            enchantment_catalog=catalog,
            planner=ItemEnchantmentsPlanner(),
        )
        return use_case, uow, reader, catalog

    async def test_plans_all_items_and_uses_one_bulk_update_and_commit(self) -> None:
        enchantment_ids = [1107, 1074, 198, 3833, 34]
        use_case, uow, reader, catalog = self.build_use_case(
            enchantment_ids=enchantment_ids,
            known_ids=set(enchantment_ids),
            items=[
                equipment_item(
                    663805,
                    0,
                    {
                        EnchantmentSlot.PROPERTY_1.value: 343,
                        EnchantmentSlot.PROPERTY_2.value: 353,
                    },
                    random_property_id=123,
                ),
                equipment_item(663806, 1),
            ],
        )

        result = await use_case.execute(character_id=1305)

        self.assertEqual(reader.requested_classes, ["rogue"])
        self.assertEqual(uow.characters.calls, 1)
        self.assertEqual(uow.character_inventory.calls, 1)
        self.assertEqual(len(uow.item_instance.bulk_calls), 1)
        self.assertEqual(len(uow.item_instance.bulk_calls[0]), 2)
        self.assertEqual(uow.commit_count, 1)
        self.assertEqual(result.updated_item_count, 2)
        self.assertEqual(result.skipped_enchantment_count, 2)
        self.assertTrue(result.persisted)

        first_item = result.items[0]
        self.assertEqual(
            [applied.slot for applied in first_item.applied],
            [
                EnchantmentSlot.PROPERTY_3,
                EnchantmentSlot.PROPERTY_4,
                EnchantmentSlot.PROPERTY_5,
            ],
        )
        self.assertEqual(first_item.skipped_enchantment_ids, (3833, 34))

        # Definitions are resolved once per unique ID, before item planning.
        self.assertEqual(catalog.calls, enchantment_ids)

    async def test_overwrite_replaces_slots_7_to_11_and_clears_unused_slots(self) -> None:
        enchantment_ids = [1107, 1074, 198]
        use_case, uow, _, _ = self.build_use_case(
            enchantment_ids=enchantment_ids,
            known_ids=set(enchantment_ids),
            items=[
                equipment_item(
                    663805,
                    0,
                    {
                        EnchantmentSlot.PROPERTY_1.value: 343,
                        EnchantmentSlot.PROPERTY_2.value: 353,
                        EnchantmentSlot.PROPERTY_3.value: 999,
                        EnchantmentSlot.PROPERTY_4.value: 888,
                        EnchantmentSlot.PROPERTY_5.value: 777,
                    },
                    random_property_id=123,
                ),
            ],
        )

        result = await use_case.execute(
            character_id=1305,
            overwrite=True,
        )

        plan = result.items[0]
        parsed = ItemEnchantments.from_string(plan.new_enchantments)

        self.assertEqual(
            [parsed.get(slot).enchantment_id for slot in ItemEnchantments.CUSTOM_SLOTS],
            [1107, 1074, 198, 0, 0],
        )
        self.assertEqual(
            [entry.slot for entry in plan.applied],
            [
                EnchantmentSlot.PROPERTY_1,
                EnchantmentSlot.PROPERTY_2,
                EnchantmentSlot.PROPERTY_3,
            ],
        )
        self.assertEqual(
            plan.cleared_slots,
            (
                EnchantmentSlot.PROPERTY_4,
                EnchantmentSlot.PROPERTY_5,
            ),
        )
        self.assertEqual(plan.skipped_enchantment_ids, ())
        self.assertEqual(len(uow.item_instance.bulk_calls), 1)
        self.assertEqual(uow.commit_count, 1)

    async def test_overwrite_skips_enchantments_above_five_slots(self) -> None:
        enchantment_ids = [1107, 1074, 198, 3833, 34, 195]
        use_case, _, _, _ = self.build_use_case(
            enchantment_ids=enchantment_ids,
            known_ids=set(enchantment_ids),
            items=[equipment_item(663805, 0)],
        )

        result = await use_case.execute(
            character_id=1305,
            overwrite=True,
            dry_run=True,
        )

        plan = result.items[0]
        self.assertEqual(len(plan.applied), 5)
        self.assertEqual(plan.skipped_enchantment_ids, (195,))

    async def test_dry_run_calculates_without_bulk_update(self) -> None:
        use_case, uow, _, _ = self.build_use_case(
            enchantment_ids=[1107, 1074],
            known_ids={1107, 1074},
            items=[equipment_item(663805, 0)],
        )

        result = await use_case.execute(
            character_id=1305,
            dry_run=True,
        )

        self.assertEqual(uow.item_instance.bulk_calls, [])
        self.assertEqual(uow.commit_count, 0)
        self.assertEqual(result.updated_item_count, 1)
        self.assertFalse(result.persisted)

    async def test_duplicate_ids_are_looked_up_once_but_applied_twice(self) -> None:
        use_case, _, _, catalog = self.build_use_case(
            enchantment_ids=[1107, 1107],
            known_ids={1107},
            items=[equipment_item(663805, 0)],
        )

        result = await use_case.execute(
            character_id=1305,
            dry_run=True,
        )

        self.assertEqual(catalog.calls, [1107])
        self.assertEqual(
            [entry.enchantment.enchantment_id for entry in result.items[0].applied],
            [1107, 1107],
        )

    async def test_unknown_enchantment_aborts_before_inventory_query(self) -> None:
        use_case, uow, _, _ = self.build_use_case(
            enchantment_ids=[1107, 999999],
            known_ids={1107},
            items=[equipment_item(663805, 0)],
        )

        with self.assertRaises(EnchantmentNotFoundError):
            await use_case.execute(character_id=1305)

        self.assertEqual(uow.character_inventory.calls, 0)
        self.assertEqual(uow.item_instance.bulk_calls, [])
        self.assertEqual(uow.commit_count, 0)


if __name__ == "__main__":
    unittest.main()
