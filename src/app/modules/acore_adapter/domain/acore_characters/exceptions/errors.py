from app.common.errors.base_exceptions import AppError, ValidationError, NotFoundError
from enum import StrEnum

class CharacterCatalogErrorMessages(StrEnum):
    BASE_CHARACTER_ERROR_MESSAGE = "Character error"
    CHARACTER_VALIDATION_ERROR = "Character validation error"
    CHARACTER_EMPTY_NAME_ERROR = "Character name cannot be empty"
    CHARACTER_LEVEL_REQIRED_ERROR = "Character level must be between 1 and 80"
    CHARACTER_NOT_FOUND_ERROR = "Character not found"
    CHARACTER_IS_ONLINE_ERROR = "Current character is online"
    
class CharacterCatalogErrorCodes(StrEnum):
    BASE_CHARACTER_ERROR_CODE = "character.error"
    CHARACTER_VALIDATION_ERROR_CODE = "chararcet.validation.error"
    CHARACTER_EMPTY_NAME_ERROR_CODE = "character.validation.empty_name.error"
    CHARACTER_LEVEL_REQIRED_ERROR_CODE = "character.validation.level_required.error"
    CHARACTER_NOT_FOUND_ERROR_CODE = "character.not_found.error"
    CHARACTER_IS_ONLINE_ERROR_CODE = "character.is_online_error"
    
class BaseCharacterError(AppError):
    message = CharacterCatalogErrorMessages.BASE_CHARACTER_ERROR_MESSAGE.value
    code = CharacterCatalogErrorCodes.BASE_CHARACTER_ERROR_CODE.value
    
class CharacterValidationError(ValidationError):
    message = CharacterCatalogErrorMessages.CHARACTER_VALIDATION_ERROR.value
    code = CharacterCatalogErrorCodes.CHARACTER_VALIDATION_ERROR_CODE.value
    
class CharacterNameEmptyError(CharacterValidationError):
    message = CharacterCatalogErrorMessages.CHARACTER_EMPTY_NAME_ERROR.value
    code = CharacterCatalogErrorCodes.CHARACTER_EMPTY_NAME_ERROR_CODE.value
    
class CharacterLevelRequiredError(CharacterValidationError):
    message = CharacterCatalogErrorMessages.CHARACTER_LEVEL_REQIRED_ERROR.value
    code = CharacterCatalogErrorCodes.CHARACTER_LEVEL_REQIRED_ERROR_CODE.value
    
    
class CharacterNotFoundError(NotFoundError):
    message = CharacterCatalogErrorMessages.CHARACTER_NOT_FOUND_ERROR.value
    code = CharacterCatalogErrorCodes.CHARACTER_NOT_FOUND_ERROR_CODE.value
    
class CharacterIsOnlineError(BaseCharacterError):
    message = CharacterCatalogErrorMessages.CHARACTER_IS_ONLINE_ERROR.value
    code = CharacterCatalogErrorCodes.CHARACTER_IS_ONLINE_ERROR_CODE.value
    