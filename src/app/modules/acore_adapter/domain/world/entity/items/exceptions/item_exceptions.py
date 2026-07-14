from enum import StrEnum
from app.common.errors.base_exceptions import AppError, NotFoundError, InfrastructureError, ValidationError, ConflictError

class ItemErrorCatalogMessages(StrEnum):
    ITEM_APP_ERROR = "Item app error"
    ITEM_NOT_FOUND_ERROR = "Item not found in database"
    ITEM_INFRASTRUCTURE_ERROR = "Item's infrastructure error"
    ITEM_VALIDATION_ERROR = "Item validation error"
    ITEM_CONFLICT_ERROR = "Item conflict error"
    
class ItemErrorCodesCatalog(StrEnum):
    ITEM_APP_ERROR = "item.app.error"
    ITEM_NOT_FOUND_ERROR = "item.not_found.error"
    ITEM_INFRASTRUCTURE_ERROR = "item.infrastructure.error"
    ITEM_VALIDATION_ERROR = "item.validation.error"
    ITEM_CONFLICT_ERROR = "item.conflict.error"
    
class ItemAppError(AppError):
    message = ItemErrorCatalogMessages.ITEM_APP_ERROR
    code = ItemErrorCodesCatalog.ITEM_APP_ERROR
    
class ItemNotFoundError(NotFoundError):
    message = ItemErrorCatalogMessages.ITEM_NOT_FOUND_ERROR
    code = ItemErrorCodesCatalog.ITEM_NOT_FOUND_ERROR
    
class ItemInfrastructureError(InfrastructureError):
    message = ItemErrorCatalogMessages.ITEM_INFRASTRUCTURE_ERROR
    code = ItemErrorCodesCatalog.ITEM_INFRASTRUCTURE_ERROR
    
class ItemValidationError(ValidationError):
    message = ItemErrorCatalogMessages.ITEM_VALIDATION_ERROR
    code = ItemErrorCodesCatalog.ITEM_VALIDATION_ERROR
    
class ItemConflictError(ConflictError):
    message = ItemErrorCatalogMessages.ITEM_CONFLICT_ERROR
    code = ItemErrorCodesCatalog.ITEM_CONFLICT_ERROR                