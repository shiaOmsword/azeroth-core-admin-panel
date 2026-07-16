from app.config.settings import settings
from pathlib import Path
import yaml

class YamlSetsReader:
    def __init__(self, path:Path):
        self.path = path
        self._sets = self._load()
        
    def _load(self) -> dict:
        with settings.enchantments_set_catalog.open("r", encoding="utf-8") as file:
            sets = yaml.safe_load(file)
        return sets
    
    def get_enchant_set(self, character_class:str) -> list[int]:
        return self._sets["sets"][character_class]
