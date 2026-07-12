CHARACTER_GENDERS: dict[int, str] = {
    1: "female",
    0: "male",
}


def get_character_gender_name(gender_id: int) -> str:
    return CHARACTER_GENDERS.get(gender_id, "undefined")