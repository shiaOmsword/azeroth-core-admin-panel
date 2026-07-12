from typing import Type, TypeVar
from app.modules.acore_adapter.application.auth.realmlist.use_cases.get_all import ListRealmlistsUseCase
from app.modules.acore_adapter.application.auth.realmlist.use_cases.set_addres import SetRealmlistAddresUseCase

T = TypeVar("T")
AUTH_USECASES_GROUP:dict[str, Type[T]] = {
    "list": ListRealmlistsUseCase,
    "set": SetRealmlistAddresUseCase,
}

__all__ = [
    "ListRealmlistsUseCase",
    "SetRealmlistAddresUseCase",
    "AUTH_USECASES_GROUP",
]