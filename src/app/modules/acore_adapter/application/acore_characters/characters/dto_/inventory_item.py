from dataclasses import dataclass

@dataclass
class InventoryItem:
    slot:int
    item_instance_id:int
    name:str
