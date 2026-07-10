import asyncio
import logging
from app.config.settings import settings
from app.common.logging.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)
from app.common.cli.cli import app

async def start() -> None:
    logger.info("Current dev environment:[red] %s[/red]", settings.environment)
    logger.info("Building app deps")
    logger.info("[green]Builded app deps[/green]")
    logger.info("[blue]Start WoW admin panel[/blue]")
    
    # id = 21
    # logger.info("[indigo]Try to get character[/indigo] by id: %s", id)
    # get_by_id_use_case = container.resolve(GetCharacterByIdUseCase)
    # character = await get_by_id_use_case.execute(id)
    # logger.info("Character: %s", character)
    
    
def main() -> None:
    asyncio.run(start())
    app()    
    