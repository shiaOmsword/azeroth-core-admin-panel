# application/remote/commands.py

class WorldCommands:
    @staticmethod
    def server_info() -> str:
        return "server info"

    @staticmethod
    def account_online_list() -> str:
        return "account onlinelist"

    @staticmethod
    def set_character_level(
        character_name: str,
        level: int,
    ) -> str:
        return f"character level {character_name} {level}"

    @staticmethod
    def add_item(
        character_name: str,
        item_id: int,
        count: int = 1,
    ) -> str:
        return f"send items {character_name} item:{item_id}:{count}"

    @staticmethod
    def send_money(
        character_name: str,
        amount: int,
    ) -> str:
        return f"send money {character_name} {amount}"