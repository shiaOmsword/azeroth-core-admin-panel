from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


@dataclass
class AuthSessionProvider:
    sessionmaker: async_sessionmaker[AsyncSession]

    def __call__(self) -> AsyncSession:
        return self.sessionmaker()


@dataclass
class CharactersSessionProvider:
    sessionmaker: async_sessionmaker[AsyncSession]

    def __call__(self) -> AsyncSession:
        return self.sessionmaker()


@dataclass
class WorldSessionProvider:
    sessionmaker: async_sessionmaker[AsyncSession]

    def __call__(self) -> AsyncSession:
        return self.sessionmaker()