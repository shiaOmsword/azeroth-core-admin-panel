from app.common.errors.base_exceptions import AppError
from enum import StrEnum
from httpx import RequestError
class WorldServerMessagesCatalog(StrEnum):
    WORLD_SERVER_SOAP_ERROR_MESSAGE = "World server soap error message"
    WORLD_SERVER_SOAP_CONNECTION_ERROR_MESSAGE = "Cannot connect to worldserver SOAP. URL={url!r}. Error={error_name}: {error!r}"
    WORLD_SERVER_SOAP_PARSER_ERROR_MESSAGE = "Invalid SOAP XML response. Status={status_code}. Body={xml}"
    WORLD_SERVER_SOAP_UNKNOWN_FAULT_MESSAGE = "Unknown SOAP fault"
    WORLD_SERVER_SOAP_UNEXPECTED_RESPONSE_MESSAGE = "Unexpected SOAP response. Status={status_code}. Body={xml} "
    
class WorldServerErrorCodesCatalog(StrEnum):
    WORLD_SERVER_SOAP_ERROR_CODE = "world_server.soap.error"
    WORLD_SERVER_SOAP_CONNECTION_ERROR_CODE = "world_server.soap.connection.error"
    WORLD_SERVER_SOAP_PARSER_ERROR_CODE = "world_server.soap.parser.error"
    WORLD_SERVER_SOAP_UNKNOWN_FAULT_CODE = "world_server.soap.unknown_fault.error"
    WORLD_SERVER_SOAP_UNEXPECTED_RESPONSE_ERROR_CODE = "world_server.soap.unexpected.error"
    
class WorldserverSoapError(AppError):
    message = WorldServerMessagesCatalog.WORLD_SERVER_SOAP_ERROR_MESSAGE.value
    code = WorldServerErrorCodesCatalog.WORLD_SERVER_SOAP_ERROR_CODE.value

class WorldserverSoapConnectionError(WorldserverSoapError):
    def __init__(
        self, 
        url:str,
        error_name:str,
        error:RequestError,
    ) -> None:
        message = (
            WorldServerMessagesCatalog
            .WORLD_SERVER_SOAP_CONNECTION_ERROR_MESSAGE
            .format(
                url=url,
                error_name=error_name,
                error=error,
            )
        )
        
        code = (
            WorldServerErrorCodesCatalog
            .WORLD_SERVER_SOAP_CONNECTION_ERROR_CODE
            .value
        )
        
        super().__init__(
            message=message,
            code=code,
        )

class WorldserverSoapCommandError(WorldserverSoapError):
    def __init__(self,xml:str, status_code:str):
        message = (
            WorldServerMessagesCatalog
            .WORLD_SERVER_SOAP_UNEXPECTED_RESPONSE_MESSAGE
            .format(
                status_code=status_code,
                xml=xml
            )
        )
        code = (
            WorldServerErrorCodesCatalog
            .WORLD_SERVER_SOAP_UNEXPECTED_RESPONSE_ERROR_CODE
            .value
        )
        super().__init__(
            message=message, 
            code=code,
        )

class WorldServerCommandParserError(WorldserverSoapError):
    def __init__(self,
        status_code:str,
        xml:str
    ):
        message = (
            WorldServerMessagesCatalog
            .WORLD_SERVER_SOAP_PARSER_ERROR_MESSAGE
            .format(
                status_code=status_code,
                xml=xml,
            )
        )
        code = (
            WorldServerErrorCodesCatalog
            .WORLD_SERVER_SOAP_PARSER_ERROR_CODE
            .value
        )
        
        super().__init__(
            message=message,
            code=code,
        )
    

class WorldServerCommandSoapFaultError(WorldserverSoapError):
    def __init__(
        self,
        text:str | None = None,
    ):
        message = text or (
            WorldServerMessagesCatalog
            .WORLD_SERVER_SOAP_UNKNOWN_FAULT_MESSAGE
            .value
        )
        code = (
            WorldServerErrorCodesCatalog
            .WORLD_SERVER_SOAP_UNKNOWN_FAULT_CODE
            .value
        )
        super().__init__(
            message=message,
            code=code
        )