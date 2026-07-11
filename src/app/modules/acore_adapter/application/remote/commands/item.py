    
class ItemWorldCommands:
    @staticmethod
    def add_item(
        character_name: str,
        item_id: int,
        count: int = 1,
    ) -> str:
        return f"send items {character_name} item:{item_id}:{count}"