class EnchantmentError(Exception):
    """Base error for item enchantment operations."""


class ItemInstanceNotFoundError(EnchantmentError):
    pass


class ItemOwnerNotFoundError(EnchantmentError):
    pass


class EnchantmentNotFoundError(EnchantmentError):
    pass


class EnchantmentSlotOccupiedError(EnchantmentError):
    pass


class ReservedEnchantmentSlotError(EnchantmentError):
    pass


class NoFreeCustomEnchantmentSlotError(EnchantmentError):
    pass


class InvalidEnchantmentsFormatError(EnchantmentError):
    pass


class NativeRandomPropertyConflictError(EnchantmentError):
    pass


class CharacterOnlineError(EnchantmentError):
    pass
