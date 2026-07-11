from __future__ import annotations
from enum import StrEnum

class BaseErrorsMessagesCatalog(StrEnum):
    APP_ERROR_MESSAGE = "Application error"
    VALIDATION_ERROR_MESSAGE = "Invalid input data"
    NOT_FOUND_ERROR_MESSAGE = "Entity not found"
    CONFLICT_ERROR_MESSAGE = "Conflict"
    EXTERNAL_SERVICE_ERROR_MESSAGE = "External service error"
    INFRASTRUCTURE_ERROR_MESSAGE = "Infrastrcture error"
    UNIT_OF_WORK_ERROR_MESSAGE = "Unit of work is not active"

class BaseErrorsCodesCatalog(StrEnum):
    APP_ERROR_CODE = "app.error"
    VALIDATION_ERROR_CODE = "validation.error"
    NOT_FOUND_ERROR_CODE = "entity.not_found.error"
    CONFLICT_ERROR_CODE = "conflict.error"
    EXTERNAL_SERVICE_ERROR_CODE = "external.service.error"
    INFRASTRUCTURE_ERROR_CODE = "infrastrcture.error"
    UNIT_OF_WORK_ERROR_CODE = "uow.not_active.error"

class AppError(Exception):
    """Base error class"""
    message:str = BaseErrorsMessagesCatalog.APP_ERROR_MESSAGE.value
    code:str = BaseErrorsCodesCatalog.APP_ERROR_CODE.value
    def __init__(
        self, 
        message:str | None = None,
        code:str | None = None
    ) -> None:
        self.message = message or self.message
        self.code = code or self.code
        super().__init__(
            self.message,
            self.code,
        )
        
class ValidationError(AppError):
    """Input validation error"""
    message = BaseErrorsMessagesCatalog.VALIDATION_ERROR_MESSAGE.value
    code:str = BaseErrorsCodesCatalog.VALIDATION_ERROR_CODE.value
class NotFoundError(AppError):
    """Entity not found"""
    message = BaseErrorsMessagesCatalog.NOT_FOUND_ERROR_MESSAGE.value
    code:str = BaseErrorsCodesCatalog.NOT_FOUND_ERROR_CODE.value
    
class ConflictError(AppError):
    """Integrity conflict"""
    message = BaseErrorsMessagesCatalog.CONFLICT_ERROR_MESSAGE.value
    code:str = BaseErrorsCodesCatalog.CONFLICT_ERROR_CODE.value
class ExternalServiceError(AppError):
    """External api error"""
    message = BaseErrorsMessagesCatalog.EXTERNAL_SERVICE_ERROR_MESSAGE.value
    code:str = BaseErrorsCodesCatalog.EXTERNAL_SERVICE_ERROR_CODE.value
    
class InfrastructureError(AppError):
    """Infrastructure error: database, filesystem etc..."""
    message = BaseErrorsMessagesCatalog.INFRASTRUCTURE_ERROR_MESSAGE.value
    code:str = BaseErrorsCodesCatalog.INFRASTRUCTURE_ERROR_CODE.value
    
class UowActivationError(AppError):
    """Unit of work not active error"""
    message = BaseErrorsMessagesCatalog.UNIT_OF_WORK_ERROR_MESSAGE.value
    code:str = BaseErrorsCodesCatalog.UNIT_OF_WORK_ERROR_CODE.value