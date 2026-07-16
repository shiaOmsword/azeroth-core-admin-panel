from collections.abc import Sequence
from typing import Any, Protocol, TypeVar

from punq import Container

from app.common.bootstrap.di import BuildDi
from app.common.bootstrap.use_cases.characters import CHARACTER_USE_CASES_GROUP
from app.common.ui.console import console
from app.modules.acore_adapter.application.acore_characters.item_instances.dto.enchantments import (
    EnchantmentChange,
)
from app.modules.acore_adapter.domain.acore_characters.item_instances.enchantments import (
    EnchantmentSlot,
)


class ExecutableUseCase(Protocol):
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        ...


TUseCase = TypeVar("TUseCase", bound=ExecutableUseCase)


class AsyncUseCaseRunner:
    def __init__(self, container: Container) -> None:
        self._container = container

    async def run(
        self,
        use_case_type: type[TUseCase],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        use_case = self._container.resolve(use_case_type)
        response = await use_case.execute(*args, **kwargs)
        console.print(response)
        return response


container = BuildDi().build()
runner = AsyncUseCaseRunner(container=container)


async def async_list_characters(page: int = 0) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["list"],
        page=page,
    )


async def async_get_character_by_account_id(account_id: int) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["get_by_account_id"],
        account_id=account_id,
    )


async def async_get_character_by_name(name: str) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["get_by_character_name"],
        name=name,
    )


async def set_talents(char_id: int, value: int) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["set_extra_talent_points"],
        character_id=char_id,
        value=value,
    )


async def change_name(char_id: int, value: str) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["change_name"],
        char_id=char_id,
        value=value,
    )


async def get_raw_character_inventory(character_id: int) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["character_inventory"],
        character_id=character_id,
    )


async def get_item_enchantments(item_instance_id: int) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["item_enchantments"],
        item_instance_id=item_instance_id,
    )


async def apply_item_enchantment(
    item_instance_id: int,
    enchantment_id: int,
    slot: int | None = None,
    overwrite: bool = False,
    dry_run: bool = False,
) -> None:
    parsed_slot = EnchantmentSlot(slot) if slot is not None else None
    await runner.run(
        CHARACTER_USE_CASES_GROUP["apply_item_enchantment"],
        item_instance_id=item_instance_id,
        enchantment_id=enchantment_id,
        slot=parsed_slot,
        overwrite=overwrite,
        dry_run=dry_run,
    )


async def apply_item_enchantments(
    item_instance_id: int,
    changes: Sequence[EnchantmentChange],
    dry_run: bool = False,
) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["apply_item_enchantments"],
        item_instance_id=item_instance_id,
        changes=changes,
        dry_run=dry_run,
    )


async def get_character_inventory(character_id: int) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["inventory_o"],
        character_id=character_id,
    )
    
async def auto_apply_enchants(
    character_id: int,
    dry_run: bool = False,
) -> None:
    await runner.run(
        CHARACTER_USE_CASES_GROUP["auto_enchants"],
        character_id=character_id,
        dry_run=dry_run,
    )


ASYNC_FUNCS_CHARACTERS_GROUP = {
    "list": async_list_characters,
    "get_by_account_id": async_get_character_by_account_id,
    "get_by_character_name": async_get_character_by_name,
    "set_extra_talent_points": set_talents,
    "change_name": change_name,
    "inventory": get_character_inventory,
    "character_inventory": get_raw_character_inventory,
    "item_enchantments": get_item_enchantments,
    "apply_item_enchantment": apply_item_enchantment,
    "apply_item_enchantments": apply_item_enchantments,
    "auto_apply_enchants":auto_apply_enchants,
}
