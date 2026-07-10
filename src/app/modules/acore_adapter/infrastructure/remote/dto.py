# app/modules/acore_adapter/infrastructure/remote/dto.py

from dataclasses import dataclass


@dataclass(frozen=True)
class WorldCommandResult:
    command: str
    raw_response: str