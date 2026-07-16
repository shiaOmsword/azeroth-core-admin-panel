from dataclasses import dataclass
from enum import IntEnum
from collections.abc import Iterator

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
    enchantment_id: int = 0
    duration: int = 0
    charges: int = 0


class ItemEnchantments:
    SLOT_COUNT = 12
    VALUES_PER_SLOT = 3

    def __init__(self, values: list[EnchantmentValue]) -> None:
        if len(values) != self.SLOT_COUNT:
            raise ValueError(
                f"Expected {self.SLOT_COUNT} enchantment slots, "
                f"got {len(values)}"
            )

        self._values = values

    @classmethod
    def from_string(cls, raw: str) -> "ItemEnchantments":
        numbers = [int(value) for value in raw.split()]

        expected = cls.SLOT_COUNT * cls.VALUES_PER_SLOT

        if len(numbers) != expected:
            raise ValueError(
                f"Expected {expected} enchantment values, got {len(numbers)}"
            )

        slots = [
            EnchantmentValue(
                enchantment_id=numbers[index],
                duration=numbers[index + 1],
                charges=numbers[index + 2],
            )
            for index in range(0, expected, cls.VALUES_PER_SLOT)
        ]

        return cls(slots)

    def get(self, slot: EnchantmentSlot) -> EnchantmentValue:
        return self._values[slot.value]

    def set_custom(
        self,
        slot: EnchantmentSlot,
        enchantment_id: int,
        *,
        overwrite: bool = False,
    ) -> None:
        allowed_slots = {
            EnchantmentSlot.PROPERTY_1,
            EnchantmentSlot.PROPERTY_2,
            EnchantmentSlot.PROPERTY_3,
            EnchantmentSlot.PROPERTY_4,
            EnchantmentSlot.PROPERTY_5,
        }

        if slot not in allowed_slots:
            raise ValueError(
                f"Slot {slot.name} is reserved by AzerothCore"
            )

        current = self.get(slot)

        if current.enchantment_id != 0 and not overwrite:
            raise ValueError(
                f"Slot {slot.value} already contains "
                f"enchantment {current.enchantment_id}"
            )

        self._values[slot.value] = EnchantmentValue(
            enchantment_id=enchantment_id,
            duration=0,
            charges=0,
        )

    def serialize(self) -> str:
        values: list[str] = []

        for slot in self._values:
            values.extend(
                (
                    str(slot.enchantment_id),
                    str(slot.duration),
                    str(slot.charges),
                )
            )

        return " ".join(values) + " "
    
    
    def items(
        self,
    ) -> Iterator[tuple[EnchantmentSlot, EnchantmentValue]]:
        for slot in EnchantmentSlot:
            yield slot, self._values[slot.value]

    def active(
        self,
    ) -> Iterator[tuple[EnchantmentSlot, EnchantmentValue]]:
        for slot, enchantment in self.items():
            if enchantment.enchantment_id != 0:
                yield slot, enchantment    