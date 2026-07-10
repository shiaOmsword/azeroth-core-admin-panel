# app/modules/acore_adapter/infrastructure/remote/factory.py

from app.config.settings import settings
from app.modules.acore_adapter.infrastructure.remote.soap_client import AcoreSoapClient


def build_acore_soap_client() -> AcoreSoapClient:
    return AcoreSoapClient(
        base_url=settings.acore_soap_url,
        username=settings.acore_soap_username,
        password=settings.acore_soap_password,
        timeout=settings.acore_soap_timeout,
    )