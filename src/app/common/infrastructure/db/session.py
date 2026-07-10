# app/common/db/session.py

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.common.infrastructure.db.engines import (
    world_engine, 
    auth_engine, 
    characters_engine,
)


auth_session_factory = async_sessionmaker(
    bind=auth_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

characters_session_factory = async_sessionmaker(
    bind=characters_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

world_session_factory = async_sessionmaker(
    bind=world_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_auth_session() -> AsyncGenerator[AsyncSession, None]:
    async with auth_session_factory() as session:
        yield session
        
        
async def get_world_session() -> AsyncGenerator[AsyncSession, None]:
    async with world_session_factory() as session:
        yield session
        
async def get_characters_session() -> AsyncGenerator[AsyncSession, None]:
    async with characters_session_factory() as session:
        yield session                
        