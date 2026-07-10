# app/common/db/engine.py

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config.settings import settings



auth_engine = create_async_engine(
    settings.wow_auth_db_url,
    echo=settings.db_echo,
    pool_pre_ping=True,
)

characters_engine = create_async_engine(
    settings.wow_characters_db_url,
    echo=settings.db_echo,
    pool_pre_ping=True,
)

world_engine = create_async_engine(
    settings.wow_world_db_url,
    echo=settings.db_echo,
    pool_pre_ping=True,
)

# def create_engine() -> AsyncEngine:
#     return create_async_engine(
#         settings.database_url,
#         echo=settings.db_echo,
#         pool_size=settings.db_pool_size,
#         max_overflow=settings.db_max_overflow,
#         pool_timeout=settings.db_pool_timeout,
#         pool_pre_ping=True,
#     )
