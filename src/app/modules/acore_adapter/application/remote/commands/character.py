class CharacterWorldCommands:
    @staticmethod
    def set_character_level(
        character_name: str,
        level: int,
    ) -> str:
        return f"character level {character_name} {level}"

    @staticmethod
    def send_money(
        character_name: str,
        amount: int,
    ) -> str:
        return f"send money {character_name} {amount}"