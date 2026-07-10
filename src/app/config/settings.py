from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
ENV_FILE = BASE_DIR / ".env"
class Settings(BaseSettings):
    
    environment:str = Field(default="settings_local_environment", alias="ENVIRONMENT")
    
    #database
    db_echo: bool = Field(
        default=False,
        alias="DB_ECHO"
    )
    db_pool_size: int = Field(
        default=5,
        alias="DB_POOL_SIZE"
    )
    db_max_overflow: int = Field(
        default=10,
        alias="DB_MAX_OVERFLOW"
    )
    db_pool_timeout: int = Field(
        default=30,
        alias="DB_POOL_TIMEOUT"
    )
    
    wow_auth_db_url: str = Field(
        default="mysql+asyncmy://acore:password@127.0.0.1:3306/acore_auth",
        alias="WOW_AUTH_DB_URL"
    )
    wow_characters_db_url: str = Field(
        default="mysql+asyncmy://acore:password@127.0.0.1:3306/acore_characters",
        alias="WOW_CHARACTERS_DB_URL"
    )
    wow_world_db_url: str = Field(
        default="mysql+asyncmy://acore:password@127.0.0.1:3306/acore_world",
        alias="WOW_WORLD_DB_URL"
    )
    
    #soap
    acore_soap_url: str = Field(
        default="http://127.0.0.1:7878/",
        alias="ACORE_SOAP_URL"
    )
    acore_soap_username: str = Field(
        default="admin",
        alias="ACORE_SOAP_USERNAME"
    )
    acore_soap_password: str = Field(
        default="strong_password",
        alias="ACORE_SOAP_PASSWORD"
    )
    acore_soap_timeout: float = Field(
        default=10.0,
        alias="ACORE_SOAP_TIMEOUT"
    )
        
    model_config = SettingsConfigDict (
        env_file=f"{ENV_FILE}",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )
    
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()