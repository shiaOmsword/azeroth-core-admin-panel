import httpx
import html
import xml.etree.ElementTree as ET
from app.modules.acore_adapter.infrastructure.remote.exceptions import (
    WorldserverSoapCommandError,
    WorldserverSoapConnectionError,
)

from app.modules.acore_adapter.infrastructure.remote.dto import (
    WorldCommandResult,
)
class AcoreSoapClient:
    def __init__(
        self, 
        base_url: str, 
        username:str,
        password:str,
        timeout:float = 10.0
    ):
        self._base_url = base_url
        self._username = username
        self._password = password
        self._timeout = timeout
        
    async def execute(self, command: str) -> WorldCommandResult:
        envelope = self._build_envelope(command)

        try:
            async with httpx.AsyncClient(
                timeout=self._timeout,
                auth=httpx.BasicAuth(
                    self._username,
                    self._password,
                ),
                trust_env=False,
            ) as client:
                response = await client.post(
                    self._base_url,
                    content=envelope.encode("utf-8"),
                    headers={
                        "Content-Type": "text/xml; charset=utf-8",
                        "SOAPAction": '"urn:AC#executeCommand"',
                        "Connection": "close",
                    },
                )

        except httpx.RequestError as exc:
            raise WorldserverSoapConnectionError(
                "Cannot connect to worldserver SOAP. "
                f"URL={self._base_url!r}. "
                f"Error={type(exc).__name__}: {exc!r}"
            ) from exc

        return self._parse_response(
            command=command,
            xml=response.text,
            status_code=response.status_code,
        )   
            
            
    def _parse_response(
        self,
        command: str,
        xml: str,
        status_code: int,
    ) -> WorldCommandResult:
        try:
            root = ET.fromstring(xml)
        except ET.ParseError as exc:
            raise WorldserverSoapCommandError(
                f"Invalid SOAP XML response. "
                f"Status={status_code}. "
                f"Body={xml}"
            ) from exc

        for element in root.iter():
            if element.tag.endswith("faultstring"):
                raise WorldserverSoapCommandError(
                    element.text or "Unknown SOAP fault"
                )

        for element in root.iter():
            if element.tag.endswith("result"):
                return WorldCommandResult(
                    command=command,
                    raw_response=element.text or "",
                )

        raise WorldserverSoapCommandError(
            f"Unexpected SOAP response. "
            f"Status={status_code}. "
            f"Body={xml}"
        )
                    
    def _build_envelope(self, command: str) -> str:
        escaped_command = html.escape(command, quote=True)

        return (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<SOAP-ENV:Envelope '
            'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" '
            'xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
            'xmlns:ns1="urn:AC">'
            '<SOAP-ENV:Body>'
            '<ns1:executeCommand>'
            f'<command xsi:type="xsd:string">{escaped_command}</command>'
            '</ns1:executeCommand>'
            '</SOAP-ENV:Body>'
            '</SOAP-ENV:Envelope>'
        )  