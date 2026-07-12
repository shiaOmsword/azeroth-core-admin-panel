CHARACTER_CLASSES: dict[int, str] = {
    4: "rogue",
    8: "mage",
}


def get_character_classes_name(class_id: int) -> str:
    return CHARACTER_CLASSES.get(class_id, "undefined")