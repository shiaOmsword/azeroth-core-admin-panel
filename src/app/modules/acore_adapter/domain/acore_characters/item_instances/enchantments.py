from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from enum import IntEnum

from .errors import (
    EnchantmentSlotOccupiedError,
    InvalidEnchantmentsFormatError,
    NoFreeCustomEnchantmentSlotError,
    ReservedEnchantmentSlotError,
)


@dataclass(frozen=True, slots=True)
class EnchantmentDefinition:
    """Read-only description of an enchantment from the DBC catalog."""

    enchantment_id: int
    name: str
    effect_summary: str


class EnchantmentSlot(IntEnum):
    PERMANENT = 0
    TEMPORARY = 1
    SOCKET_1 = 2
    SOCKET_2 = 3
    SOCKET_3 = 4
    SOCKET_BONUS = 5
    PRISMATIC_SOCKET = 6
    PROPERTY_1 = 7
    PROPERTY_2 = 8
    PROPERTY_3 = 9
    PROPERTY_4 = 10
    PROPERTY_5 = 11


@dataclass(frozen=True, slots=True)
class EnchantmentValue:
    """The three values stored in one item_instance enchantment slot."""

    enchantment_id: int = 0
    duration: int = 0
    charges: int = 0


class ItemEnchantments:
    """Value object representing all 12 AzerothCore enchantment slots."""

    SLOT_COUNT = 12
    VALUES_PER_SLOT = 3
    CUSTOM_SLOTS = (
        EnchantmentSlot.PROPERTY_1,
        EnchantmentSlot.PROPERTY_2,
        EnchantmentSlot.PROPERTY_3,
        EnchantmentSlot.PROPERTY_4,
        EnchantmentSlot.PROPERTY_5,
    )

    def __init__(self, values: list[EnchantmentValue]) -> None:
        if len(values) != self.SLOT_COUNT:
            raise InvalidEnchantmentsFormatError(
                f"Expected {self.SLOT_COUNT} enchantment slots, got {len(values)}"
            )

        # Copy the list so callers cannot mutate our internal state indirectly.
        self._values = list(values)

    @classmethod
    def from_string(cls, raw: str) -> "ItemEnchantments":
        try:
            numbers = [int(value) for value in raw.split()]
        except ValueError as exc:
            raise InvalidEnchantmentsFormatError(
                "Enchantments string contains a non-integer value"
            ) from exc

        expected = cls.SLOT_COUNT * cls.VALUES_PER_SLOT
        if len(numbers) != expected:
            raise InvalidEnchantmentsFormatError(
                f"Expected {expected} enchantment values, got {len(numbers)}"
            )

        values = [
            EnchantmentValue(
                enchantment_id=numbers[index],
                duration=numbers[index + 1],
                charges=numbers[index + 2],
            )
            for index in range(0, expected, cls.VALUES_PER_SLOT)
        ]
        return cls(values)

    def get(self, slot: EnchantmentSlot) -> EnchantmentValue:
        return self._values[slot.value]

    def set_custom(
        self,
        slot: EnchantmentSlot,
        enchantment_id: int,
        *,
        overwrite: bool = False,
    ) -> None:
        if slot not in self.CUSTOM_SLOTS:
            raise ReservedEnchantmentSlotError(
                f"Slot {slot.name} is reserved by AzerothCore"
            )

        current = self.get(slot)
        if current.enchantment_id != 0 and not overwrite:
            raise EnchantmentSlotOccupiedError(
                f"Slot {slot.name} already contains enchantment "
                f"{current.enchantment_id}"
            )

        self._values[slot.value] = EnchantmentValue(
            enchantment_id=enchantment_id,
            duration=0,
            charges=0,
        )

    def clear_custom(self, slot: EnchantmentSlot) -> None:
        if slot not in self.CUSTOM_SLOTS:
            raise ReservedEnchantmentSlotError(
                f"Slot {slot.name} is reserved by AzerothCore"
            )

        self._values[slot.value] = EnchantmentValue()

    def clear_custom_slots(
        self,
        slots: Iterable[EnchantmentSlot] | None = None,
    ) -> None:
        target_slots = self.CUSTOM_SLOTS if slots is None else slots
        for slot in target_slots:
            self.clear_custom(slot)

    def first_free_custom_slot(self) -> EnchantmentSlot | None:
        for slot in self.CUSTOM_SLOTS:
            if self.get(slot).enchantment_id == 0:
                return slot
        return None

    def add_custom(self, enchantment_id: int) -> EnchantmentSlot:
        slot = self.first_free_custom_slot()
        if slot is None:
            raise NoFreeCustomEnchantmentSlotError(
                "All custom enchantment slots are occupied"
            )

        self.set_custom(slot=slot, enchantment_id=enchantment_id)
        return slot

    def items(self) -> Iterator[tuple[EnchantmentSlot, EnchantmentValue]]:
        for slot in EnchantmentSlot:
            yield slot, self._values[slot.value]

    def active(self) -> Iterator[tuple[EnchantmentSlot, EnchantmentValue]]:
        for slot, value in self.items():
            if value.enchantment_id != 0:
                yield slot, value

    def serialize(self) -> str:
        values: list[str] = []
        for value in self._values:
            values.extend(
                (
                    str(value.enchantment_id),
                    str(value.duration),
                    str(value.charges),
                )
            )
        return " ".join(values) + " "
