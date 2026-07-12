CHARACTER_RACES: dict[int, str] = {
    1: "human",
    10: "high elf",
}


def get_character_race_name(race_id: int) -> str:
    return CHARACTER_RACES.get(race_id, "undefined")
