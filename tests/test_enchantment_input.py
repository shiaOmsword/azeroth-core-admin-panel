import unittest

from app.common.cli.commands.characters.enchantment_input import (
    EnchantmentSetParseError,
    build_enchantment_changes,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.enchantments import (
    EnchantmentSlot,
)


class BuildEnchantmentChangesTests(unittest.TestCase):
    def test_explicit_slots_are_built_before_automatic_changes(self) -> None:
        changes = build_enchantment_changes(
            enchantment_ids=(1074, 198),
            set_values=("9:1107",),
            overwrite=True,
        )

        self.assertEqual(changes[0].slot, EnchantmentSlot.PROPERTY_3)
        self.assertEqual(changes[0].enchantment_id, 1107)
        self.assertTrue(changes[0].overwrite)
        self.assertIsNone(changes[1].slot)
        self.assertEqual(changes[1].enchantment_id, 1074)
        self.assertFalse(changes[1].overwrite)

    def test_rejects_reserved_slot(self) -> None:
        with self.assertRaises(EnchantmentSetParseError):
            build_enchantment_changes(set_values=("1:1107",))

    def test_rejects_duplicate_explicit_slot(self) -> None:
        with self.assertRaises(EnchantmentSetParseError):
            build_enchantment_changes(
                set_values=("9:1107", "9:1074"),
            )

    def test_rejects_invalid_set_format(self) -> None:
        with self.assertRaises(EnchantmentSetParseError):
            build_enchantment_changes(set_values=("9=1107",))


if __name__ == "__main__":
    unittest.main()
