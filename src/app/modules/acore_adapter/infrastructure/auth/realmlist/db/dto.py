from __future__ import annotations
from dataclasses import dataclass

@dataclass
class RealmListDTO:
    id:int
    name:str
    address:str
    localAddress:str
    
@dataclass
class RealmListsDTO:
    realmlists:list[RealmListDTO]
    count:int
    
    @classmethod
    def from_realms(cls, realmlists:list[RealmListDTO]) -> RealmListsDTO:
        return cls(
            realmlists=realmlists,
            count=len(realmlists)
        )