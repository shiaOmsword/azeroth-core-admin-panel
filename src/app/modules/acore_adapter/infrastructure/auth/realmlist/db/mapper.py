from __future__ import annotations
from app.modules.acore_adapter.infrastructure.auth.realmlist.db.models import RealmlistModel
from app.modules.acore_adapter.infrastructure.auth.realmlist.db.dto import RealmListDTO

class RealmlistMapper:
    @staticmethod
    def map_to_dto(data:RealmlistModel) -> RealmListDTO:
        if data:
            return RealmListDTO(
                id=data.id,
                name=data.name,
                address=data.address,
                localAddress=data.localAddress,
            )
        
    