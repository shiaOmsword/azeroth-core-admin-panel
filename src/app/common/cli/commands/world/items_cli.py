import asyncio
import typer
from typing import Annotated
from app.common.bootstrap.di import BuildDi
from app.common.ui.console import console
from app.common.bootstrap.use_cases.world import WORLD_USE_CASES_GROUP

app = typer.Typer(name="items")
