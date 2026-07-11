from .character import CharacterWorldCommands
from .item import ItemWorldCommands
from .server import ServerWorldCommands

WORLD_COMMAND_GROUPS = (
    CharacterWorldCommands,
    ItemWorldCommands,
    ServerWorldCommands
)

__all__ = [
    "CharacterWorldCommands",
    "ItemWorldCommands",
    "ServerWorldCommands",
    "WORLD_COMMAND_GROUPS",
]