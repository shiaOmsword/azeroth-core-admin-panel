from dataclasses import dataclass


@dataclass(frozen=True)
class WorldCommandResult:
    command: str
    raw_response: str