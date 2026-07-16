import unittest
from dataclasses import dataclass

from app.modules.acore_adapter.application.acore_characters.item_instances.dto.enchantments import (
    EnchantmentChange,
)
from app.modules.acore_adapter.application.acore_characters.item_instances.use_cases.apply_item_enchantment import (
    ApplyItemEnchantmentUseCase,
)
from app.modules.acore_adapter.application.acore_characters.item_instances.use_cases.apply_item_enchantments import (
    ApplyItemEnchantmentsUseCase,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.enchantments import (
    EnchantmentDefinition,
    EnchantmentSlot,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.errors import (
    NativeRandomPropertyConflictError,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.item_instance import (
    ItemInstance,
)


@dataclass(slots=True)
class FakeOwner:
    guid: int = 1305
    name: str = "TestCharacter"
    online: int = 0


class FakeItemInstanceRepository:
    def __init__(self, item: ItemInstance) -> None:
        self.item = item
        self.updates: list[tuple[int, str]] = []

    async def get(self, instance_guid: int) -> ItemInstance | None:
        if instance_guid != self.item.guid:
            return None
        return self.item

    async def update_enchantments(
        self,
        item_instance_id: int,
        enchantments: str,
    ) -> None:
        self.updates.append((item_instance_id, enchantments))


class FakeCharacterRepository:
    def __init__(self, owner: FakeOwner) -> None:
        self.owner = owner

    async def get_by_guid(self, guid: int) -> FakeOwner | None:
        if guid != self.owner.guid:
            return None
        return self.owner


class FakeCharactersUnitOfWork:
    def __init__(self, item: ItemInstance, owner: FakeOwner) -> None:
        self.item_instance = FakeItemInstanceRepository(item)
        self.characters = FakeCharacterRepository(owner)
        self.commit_count = 0

    async def __aenter__(self) -> "FakeCharactersUnitOfWork":
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


class FakeEnchantmentCatalog:
    def __init__(self, known_ids: set[int]) -> None:
        self.known_ids = known_ids

    def get(self, enchantment_id: int) -> EnchantmentDefinition | None:
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


class ApplyItemEnchantmentsUseCaseTests(unittest.IsolatedAsyncioTestCase):
    def build_use_case(
        self,
        *,
        random_property_id: int = 123,
        slots: dict[int, int] | None = None,
        known_ids: set[int] | None = None,
    ) -> tuple[ApplyItemEnchantmentsUseCase, FakeCharactersUnitOfWork]:
        item = ItemInstance(
            guid=663805,
            item_entry=12044,
            owner_guid=1305,
            count=1,
            enchantments=enchantments_string(slots),
            random_property_id=random_property_id,
            played_time=0,
        )
        uow = FakeCharactersUnitOfWork(item=item, owner=FakeOwner())
        use_case = ApplyItemEnchantmentsUseCase(
            uow_factory=FakeUnitsOfWork(uow),
            enchantment_catalog=FakeEnchantmentCatalog(
                known_ids or {1107, 1074, 198}
            ),
        )
        return use_case, uow

    async def test_applies_batch_to_next_free_slots_with_one_update(self) -> None:
        use_case, uow = self.build_use_case(
            slots={
                EnchantmentSlot.PROPERTY_1.value: 343,
                EnchantmentSlot.PROPERTY_2.value: 353,
            }
        )

        result = await use_case.execute(
            item_instance_id=663805,
            changes=(
                EnchantmentChange(1107),
                EnchantmentChange(1074),
                EnchantmentChange(198),
            ),
        )

        self.assertEqual(
            [change.slot for change in result.applied],
            [
                EnchantmentSlot.PROPERTY_3,
                EnchantmentSlot.PROPERTY_4,
                EnchantmentSlot.PROPERTY_5,
            ],
        )
        self.assertEqual(len(uow.item_instance.updates), 1)
        self.assertEqual(uow.commit_count, 1)
        self.assertTrue(result.persisted)

    async def test_dry_run_does_not_write_or_commit(self) -> None:
        use_case, uow = self.build_use_case(slots={})

        result = await use_case.execute(
            item_instance_id=663805,
            changes=(EnchantmentChange(1107),),
            dry_run=True,
        )

        self.assertEqual(uow.item_instance.updates, [])
        self.assertEqual(uow.commit_count, 0)
        self.assertFalse(result.persisted)

    async def test_native_occupied_slot_cannot_be_overwritten(self) -> None:
        use_case, uow = self.build_use_case(
            slots={EnchantmentSlot.PROPERTY_1.value: 343}
        )

        with self.assertRaises(NativeRandomPropertyConflictError):
            await use_case.execute(
                item_instance_id=663805,
                changes=(
                    EnchantmentChange(
                        enchantment_id=1107,
                        slot=EnchantmentSlot.PROPERTY_1,
                        overwrite=True,
                    ),
                ),
            )

        self.assertEqual(uow.item_instance.updates, [])
        self.assertEqual(uow.commit_count, 0)

    async def test_overwrites_occupied_custom_slot_without_native_property(self) -> None:
        use_case, uow = self.build_use_case(
            random_property_id=0,
            slots={EnchantmentSlot.PROPERTY_3.value: 999},
        )

        result = await use_case.execute(
            item_instance_id=663805,
            changes=(
                EnchantmentChange(
                    enchantment_id=1107,
                    slot=EnchantmentSlot.PROPERTY_3,
                    overwrite=True,
                ),
            ),
        )

        applied = result.applied[0]
        self.assertEqual(applied.slot, EnchantmentSlot.PROPERTY_3)
        self.assertEqual(applied.previous_value.enchantment_id, 999)
        self.assertEqual(applied.current_value.enchantment_id, 1107)
        self.assertEqual(len(uow.item_instance.updates), 1)
        self.assertEqual(uow.commit_count, 1)

    async def test_explicit_change_reserves_slot_before_automatic_change(self) -> None:
        use_case, _ = self.build_use_case(
            random_property_id=0,
            slots={},
        )

        result = await use_case.execute(
            item_instance_id=663805,
            changes=(
                EnchantmentChange(
                    enchantment_id=1107,
                    slot=EnchantmentSlot.PROPERTY_1,
                ),
                EnchantmentChange(enchantment_id=1074),
            ),
            dry_run=True,
        )

        self.assertEqual(
            [change.slot for change in result.applied],
            [
                EnchantmentSlot.PROPERTY_1,
                EnchantmentSlot.PROPERTY_2,
            ],
        )

    async def test_single_use_case_delegates_to_batch(self) -> None:
        batch_use_case, uow = self.build_use_case(
            random_property_id=0,
            slots={},
        )
        use_case = ApplyItemEnchantmentUseCase(batch_use_case)

        result = await use_case.execute(
            item_instance_id=663805,
            enchantment_id=1107,
            dry_run=True,
        )

        self.assertEqual(result.selected_slot, EnchantmentSlot.PROPERTY_1)
        self.assertEqual(result.enchantment_id, 1107)
        self.assertEqual(uow.item_instance.updates, [])


if __name__ == "__main__":
    unittest.main()
