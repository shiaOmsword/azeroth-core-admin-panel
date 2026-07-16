#!/usr/bin/env python3
r"""Convert WotLK 3.3.5a SpellItemEnchantment.dbc to readable JSON.

The script uses only the Python standard library.

Examples (PowerShell):

    poetry run python -m app.scripts.dbc_enchantments_to_json .\SpellItemEnchantment.dbc --output .\spell_item_enchantments.json --locale ruRU
    
    python .\dbc_enchantments_to_json.py `
        .\SpellItemEnchantment.dbc `
        --output .\spell_item_enchantments.json `
        --locale ruRU

Merge random-enchant tier/class metadata from the module SQL dump:

    python .\dbc_enchantments_to_json.py `
        .\SpellItemEnchantment.dbc `
        --output .\random_enchantments.json `
        --locale ruRU `
        --tiers-sql .\item_enchatment_random_tiers.sql `
        --only-tiered

The resulting JSON is keyed by enchantment ID for fast lookup:

    data = json.loads(Path("random_enchantments.json").read_text("utf-8"))
    enchant = data["enchantments"]["2133"]
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


WDBC_HEADER = struct.Struct("<4s4I")
WOTLK_FIELD_COUNT = 38
WOTLK_RECORD_SIZE = WOTLK_FIELD_COUNT * 4
WOTLK_RECORD = struct.Struct(f"<{WOTLK_FIELD_COUNT}I")

LOCALES: tuple[str, ...] = (
    "enUS",
    "koKR",
    "frFR",
    "deDE",
    "enCN",
    "zhCN",
    "enTW",
    "zhTW",
    "esES",
    "esMX",
    "ruRU",
    "ptPT",
    "ptBR",
    "itIT",
    "unknown_14",
    "unknown_15",
)

ENCHANTMENT_EFFECT_TYPES: dict[int, str] = {
    0: "none",
    1: "combat_spell",
    2: "weapon_damage",
    3: "equip_spell",
    4: "resistance",
    5: "stat",
    6: "totem",
    7: "use_spell",
    8: "prismatic_socket",
}

ITEM_MOD_TYPES: dict[int, str] = {
    0: "mana",
    1: "health",
    3: "agility",
    4: "strength",
    5: "intellect",
    6: "spirit",
    7: "stamina",
    12: "defense_skill_rating",
    13: "dodge_rating",
    14: "parry_rating",
    15: "block_rating",
    16: "melee_hit_rating",
    17: "ranged_hit_rating",
    18: "spell_hit_rating",
    19: "melee_crit_rating",
    20: "ranged_crit_rating",
    21: "spell_crit_rating",
    22: "melee_hit_taken_rating",
    23: "ranged_hit_taken_rating",
    24: "spell_hit_taken_rating",
    25: "melee_crit_taken_rating",
    26: "ranged_crit_taken_rating",
    27: "spell_crit_taken_rating",
    28: "melee_haste_rating",
    29: "ranged_haste_rating",
    30: "spell_haste_rating",
    31: "hit_rating",
    32: "crit_rating",
    33: "hit_taken_rating",
    34: "crit_taken_rating",
    35: "resilience_rating",
    36: "haste_rating",
    37: "expertise_rating",
    38: "attack_power",
    39: "ranged_attack_power",
    40: "feral_attack_power",
    41: "spell_healing_done",
    42: "spell_damage_done",
    43: "mana_regeneration",
    44: "armor_penetration_rating",
    45: "spell_power",
    46: "health_regeneration",
    47: "spell_penetration",
    48: "block_value",
}

RESISTANCE_TYPES: dict[int, str] = {
    0: "physical_armor",
    1: "holy_resistance",
    2: "fire_resistance",
    3: "nature_resistance",
    4: "frost_resistance",
    5: "shadow_resistance",
    6: "arcane_resistance",
}

TIER_ROW_PATTERN = re.compile(
    r"\(\s*(?P<enchant_id>\d+)\s*,\s*"
    r"(?P<tier>\d+)\s*,\s*"
    r"'(?P<item_class>[^']+)'\s*,\s*"
    r"(?P<subclass>NULL|-?\d+)\s*\)",
    re.IGNORECASE,
)


class DbcFormatError(ValueError):
    """Raised when the input is not the expected WotLK WDBC file."""


@dataclass(frozen=True)
class DbcHeader:
    magic: str
    record_count: int
    field_count: int
    record_size: int
    string_block_size: int


@dataclass(frozen=True)
class RandomTierInfo:
    tier: int
    item_class: str
    exclusive_subclass: int | None


def unsigned_to_signed_32(value: int) -> int:
    """Interpret an unsigned 32-bit DBC field as signed two's complement."""
    return value if value < 0x80000000 else value - 0x100000000


def read_c_string(block: bytes, offset: int, encoding: str) -> str:
    if offset == 0:
        return ""
    if offset < 0 or offset >= len(block):
        raise DbcFormatError(
            f"String offset {offset} is outside the string block "
            f"(size={len(block)})."
        )

    end = block.find(b"\x00", offset)
    if end == -1:
        raise DbcFormatError(
            f"String at offset {offset} is not null-terminated."
        )

    return block[offset:end].decode(encoding, errors="replace")


def read_header(data: bytes) -> DbcHeader:
    if len(data) < WDBC_HEADER.size:
        raise DbcFormatError("The file is smaller than the 20-byte WDBC header.")

    magic, record_count, field_count, record_size, string_block_size = (
        WDBC_HEADER.unpack_from(data, 0)
    )

    try:
        magic_text = magic.decode("ascii")
    except UnicodeDecodeError as exc:
        raise DbcFormatError(f"Invalid DBC magic bytes: {magic!r}") from exc

    header = DbcHeader(
        magic=magic_text,
        record_count=record_count,
        field_count=field_count,
        record_size=record_size,
        string_block_size=string_block_size,
    )

    if magic != b"WDBC":
        raise DbcFormatError(
            f"Unsupported DBC magic {magic!r}. Expected b'WDBC' from WotLK 3.3.5a."
        )
    if field_count != WOTLK_FIELD_COUNT:
        raise DbcFormatError(
            f"Unexpected field count: {field_count}. "
            f"SpellItemEnchantment.dbc for WotLK 3.3.5a must have "
            f"{WOTLK_FIELD_COUNT} fields."
        )
    if record_size != WOTLK_RECORD_SIZE:
        raise DbcFormatError(
            f"Unexpected record size: {record_size}. "
            f"Expected {WOTLK_RECORD_SIZE} bytes."
        )

    expected_size = (
        WDBC_HEADER.size
        + record_count * record_size
        + string_block_size
    )
    if len(data) < expected_size:
        raise DbcFormatError(
            f"Truncated file: header describes {expected_size} bytes, "
            f"but the file contains {len(data)} bytes."
        )

    return header


def select_description(
    localized: list[str], requested_locale: str
) -> tuple[str, str | None]:
    if requested_locale != "auto":
        try:
            requested_index = LOCALES.index(requested_locale)
        except ValueError as exc:
            supported = ", ".join(("auto", *LOCALES))
            raise ValueError(
                f"Unknown locale {requested_locale!r}. Supported: {supported}"
            ) from exc

        value = localized[requested_index]
        if value:
            return value, requested_locale

    for index, value in enumerate(localized):
        if value:
            return value, LOCALES[index]

    return "", None


def effect_argument(
    effect_type: int, argument_id: int
) -> tuple[str | None, str | None]:
    if effect_type in {1, 3, 7}:
        return "spell_id", str(argument_id) if argument_id else None
    if effect_type == 4:
        return "resistance_type", RESISTANCE_TYPES.get(
            argument_id, f"unknown_resistance_{argument_id}"
        )
    if effect_type == 5:
        return "item_mod", ITEM_MOD_TYPES.get(
            argument_id, f"unknown_item_mod_{argument_id}"
        )
    if effect_type == 8:
        return "socket", "prismatic"
    if argument_id:
        return "raw_argument", str(argument_id)
    return None, None


def build_effect_summary(
    effect_type: int,
    amount: int,
    argument_id: int,
    argument_name: str | None,
) -> str:
    effect_name = ENCHANTMENT_EFFECT_TYPES.get(
        effect_type, f"unknown_effect_{effect_type}"
    )

    if effect_type == 0:
        return ""
    if effect_type == 1:
        return f"combat proc spell {argument_id}"
    if effect_type == 2:
        return f"{amount:+d} weapon damage"
    if effect_type == 3:
        return f"equip spell {argument_id}"
    if effect_type == 4:
        return f"{amount:+d} {argument_name or 'resistance'}"
    if effect_type == 5:
        return f"{amount:+d} {argument_name or f'item_mod_{argument_id}'}"
    if effect_type == 6:
        return f"totem effect: amount={amount}, argument={argument_id}"
    if effect_type == 7:
        return f"use spell {argument_id}"
    if effect_type == 8:
        return "adds a prismatic socket"

    return f"{effect_name}: amount={amount}, argument={argument_id}"


def parse_effects(fields: tuple[int, ...]) -> list[dict[str, Any]]:
    effect_types = fields[2:5]
    amounts = tuple(unsigned_to_signed_32(value) for value in fields[5:8])
    amounts_max = tuple(unsigned_to_signed_32(value) for value in fields[8:11])
    arguments = fields[11:14]

    effects: list[dict[str, Any]] = []
    for index, (effect_type, amount, amount_max, argument_id) in enumerate(
        zip(effect_types, amounts, amounts_max, arguments, strict=True)
    ):
        if effect_type == 0 and amount == 0 and amount_max == 0 and argument_id == 0:
            continue

        argument_kind, argument_name = effect_argument(effect_type, argument_id)
        effect_name = ENCHANTMENT_EFFECT_TYPES.get(
            effect_type, f"unknown_effect_{effect_type}"
        )
        effects.append(
            {
                "index": index,
                "type_id": effect_type,
                "type": effect_name,
                "amount": amount,
                "amount_max": amount_max,
                "argument_id": argument_id,
                "argument_kind": argument_kind,
                "argument_name": argument_name,
                "summary": build_effect_summary(
                    effect_type,
                    amount,
                    argument_id,
                    argument_name,
                ),
            }
        )

    return effects


def parse_random_tiers(sql_path: Path) -> dict[int, RandomTierInfo]:
    text = sql_path.read_text(encoding="utf-8-sig", errors="replace")
    result: dict[int, RandomTierInfo] = {}

    for match in TIER_ROW_PATTERN.finditer(text):
        enchant_id = int(match.group("enchant_id"))
        subclass_text = match.group("subclass")
        info = RandomTierInfo(
            tier=int(match.group("tier")),
            item_class=match.group("item_class").upper(),
            exclusive_subclass=(
                None if subclass_text.upper() == "NULL" else int(subclass_text)
            ),
        )

        previous = result.get(enchant_id)
        if previous is not None and previous != info:
            raise ValueError(
                f"Conflicting tier rows for enchantment {enchant_id}: "
                f"{previous!r} vs {info!r}"
            )
        result[enchant_id] = info

    if not result:
        raise ValueError(
            f"No item_enchantment_random_tiers rows were found in {sql_path}."
        )

    return result


def parse_dbc(
    dbc_path: Path,
    *,
    locale: str,
    encoding: str,
    include_all_locales: bool,
) -> tuple[DbcHeader, dict[int, dict[str, Any]]]:
    data = dbc_path.read_bytes()
    header = read_header(data)

    records_start = WDBC_HEADER.size
    records_end = records_start + header.record_count * header.record_size
    string_block = data[records_end : records_end + header.string_block_size]

    enchantments: dict[int, dict[str, Any]] = {}
    for row_index in range(header.record_count):
        row_offset = records_start + row_index * header.record_size
        fields = WOTLK_RECORD.unpack_from(data, row_offset)
        enchant_id = fields[0]

        if enchant_id in enchantments:
            raise DbcFormatError(f"Duplicate enchantment ID {enchant_id} in DBC.")

        description_offsets = fields[14:30]
        localized = [
            read_c_string(string_block, offset, encoding)
            for offset in description_offsets
        ]
        description, description_locale = select_description(localized, locale)
        effects = parse_effects(fields)
        generated_summary = "; ".join(
            effect["summary"] for effect in effects if effect["summary"]
        )

        entry: dict[str, Any] = {
            "id": enchant_id,
            "name": description or generated_summary or f"enchantment_{enchant_id}",
            "description_locale": description_locale,
            "charges": unsigned_to_signed_32(fields[1]),
            "effects": effects,
            "effect_summary": generated_summary,
            "item_visual_id": fields[31],
            "flags": fields[32],
            "source_item_id": fields[33],
            "condition_id": fields[34],
            "requirements": {
                "skill_id": fields[35],
                "skill_value": fields[36],
                "level": fields[37],
            },
        }

        if include_all_locales:
            entry["localized_names"] = {
                LOCALES[index]: value
                for index, value in enumerate(localized)
                if value
            }

        enchantments[enchant_id] = entry

    return header, enchantments


def enrich_with_tiers(
    enchantments: dict[int, dict[str, Any]],
    tiers: dict[int, RandomTierInfo],
) -> list[int]:
    missing: list[int] = []
    for enchant_id, tier_info in tiers.items():
        entry = enchantments.get(enchant_id)
        if entry is None:
            missing.append(enchant_id)
            continue
        entry["random_enchant"] = asdict(tier_info)
    return sorted(missing)


def filter_only_tiered(
    enchantments: dict[int, dict[str, Any]],
    tier_ids: Iterable[int],
) -> dict[int, dict[str, Any]]:
    wanted = set(tier_ids)
    return {
        enchant_id: entry
        for enchant_id, entry in enchantments.items()
        if enchant_id in wanted
    }


def write_json(
    output_path: Path,
    *,
    dbc_path: Path,
    header: DbcHeader,
    enchantments: dict[int, dict[str, Any]],
    locale: str,
    encoding: str,
    tiers_sql: Path | None,
    tier_count: int,
    missing_tier_ids: list[int],
) -> None:
    payload = {
        "_meta": {
            "schema": "spell_item_enchantments.v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_dbc": str(dbc_path),
            "source_tiers_sql": str(tiers_sql) if tiers_sql else None,
            "requested_locale": locale,
            "string_encoding": encoding,
            "dbc_header": asdict(header),
            "exported_enchantment_count": len(enchantments),
            "tier_row_count": tier_count,
            "tier_ids_missing_in_dbc": missing_tier_ids,
        },
        "enchantments": {
            str(enchant_id): enchantments[enchant_id]
            for enchant_id in sorted(enchantments)
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Convert WotLK 3.3.5a SpellItemEnchantment.dbc to readable JSON."
        )
    )
    parser.add_argument(
        "dbc",
        type=Path,
        help="Path to SpellItemEnchantment.dbc",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("spell_item_enchantments.json"),
        help="Output JSON path (default: spell_item_enchantments.json)",
    )
    parser.add_argument(
        "--locale",
        default="auto",
        choices=("auto", *LOCALES),
        help="Preferred localized name; falls back to the first non-empty locale",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="DBC string-block encoding (default: utf-8)",
    )
    parser.add_argument(
        "--all-locales",
        action="store_true",
        help="Include every non-empty localized name in the JSON",
    )
    parser.add_argument(
        "--tiers-sql",
        type=Path,
        help=(
            "Optional item_enchantment_random_tiers.sql; adds tier, item class, "
            "and exclusive subclass metadata"
        ),
    )
    parser.add_argument(
        "--only-tiered",
        action="store_true",
        help="Export only IDs present in --tiers-sql",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.only_tiered and args.tiers_sql is None:
        parser.error("--only-tiered requires --tiers-sql")

    try:
        header, enchantments = parse_dbc(
            args.dbc,
            locale=args.locale,
            encoding=args.encoding,
            include_all_locales=args.all_locales,
        )

        tiers: dict[int, RandomTierInfo] = {}
        missing_tier_ids: list[int] = []
        if args.tiers_sql is not None:
            tiers = parse_random_tiers(args.tiers_sql)
            missing_tier_ids = enrich_with_tiers(enchantments, tiers)

            unknown_classes = sorted(
                {
                    info.item_class
                    for info in tiers.values()
                    if info.item_class not in {"ANY", "WEAPON", "ARMOR"}
                }
            )
            if unknown_classes:
                print(
                    "Warning: unknown item classes in tier SQL: "
                    + ", ".join(unknown_classes),
                    file=sys.stderr,
                )

        if args.only_tiered:
            enchantments = filter_only_tiered(enchantments, tiers)

        write_json(
            args.output,
            dbc_path=args.dbc,
            header=header,
            enchantments=enchantments,
            locale=args.locale,
            encoding=args.encoding,
            tiers_sql=args.tiers_sql,
            tier_count=len(tiers),
            missing_tier_ids=missing_tier_ids,
        )

    except (OSError, UnicodeError, ValueError, struct.error) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(
        f"Exported {len(enchantments)} enchantments to {args.output} "
        f"({header.record_count} DBC records read)."
    )
    if missing_tier_ids:
        print(
            f"Warning: {len(missing_tier_ids)} tier IDs were not present in the DBC. "
            "See _meta.tier_ids_missing_in_dbc in the JSON.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
