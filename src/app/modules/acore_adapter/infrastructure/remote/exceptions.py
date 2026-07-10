# app/modules/acore_adapter/infrastructure/remote/exceptions.py


class WorldserverSoapError(Exception):
    pass


class WorldserverSoapConnectionError(WorldserverSoapError):
    pass


class WorldserverSoapCommandError(WorldserverSoapError):
    pass