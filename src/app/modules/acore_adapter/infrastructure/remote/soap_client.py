import httpx
import html
from .dto import WorldCommandResult
from .exceptions import (
    WorldserverSoapCommandError,
    WorldserverSoapConnectionError,
)

class AcoreSoapClient:
    def __init__(
        self,
        url:str,
        username:str,
        password:str,
        timeout:float = 10.0
    )-> None:
        self.url = url
        self.username = username
        self.password = password
        self.timeout = timeout
        
    async def execute(self, command:str) -> WorldCommandResult:
        envelope = self._build_envelope(command)
        
        headers = {
            "Content-type":"text/xml; charset=utf-8",
            "SOAPAction": "urn:AC#executeCommand",
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.url,
                    content=envelope,
                    headers=headers,
                    auth=(self.username, self.password)
                )
        except httpx.RequestError as e:
            raise WorldserverSoapConnectionError(
                f"Cannot connect to worldserver SOAP: {e}"
            )from e
            
        if response.status_code >= 400:
            raise WorldserverSoapCommandError(
                f"SOAP command failed. "
                f"Status={response.status_code}. "
                f"Body={response.text}"
            )            
            
        return WorldCommandResult(
            command=command,
            raw_response=response.text,
        )
        
    def _build_envelope(self, command: str) -> str:
        escaped_command = html.escape(command, quote=True)

        return f"""
            <?xml version="1.0" encoding="utf-8"?>
            <SOAP-ENV:Envelope
                xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
                xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
                xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance"
                xmlns:xsd="http://www.w3.org/1999/XMLSchema"
                xmlns:ns1="urn:AC">
                <SOAP-ENV:Body>
                    <ns1:executeCommand>
                        <command>{escaped_command}</command>
                    </ns1:executeCommand>
                </SOAP-ENV:Body>
            </SOAP-ENV:Envelope>"""                    