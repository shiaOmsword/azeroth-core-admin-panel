from app.common.infrastructure.db.providers import AuthSessionProvider
from app.modules.acore_adapter.infrastructure.auth.realmlist.db.repository import RealmlistRepository

class AuthUnitOfWork:
    def __init__(self, auth_provider: AuthSessionProvider):
        self.auth_provider = auth_provider
        self.session = None
        self.realmlists = None

    async def __aenter__(self):
        self.session = self.auth_provider()
        self.realmlists = RealmlistRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session is None:
            return

        try:
            if exc_type:
                await self.session.rollback()
        finally:
            await self.session.close()