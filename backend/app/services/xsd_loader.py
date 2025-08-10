from pathlib import Path
import xmlschema
from ..config import settings

class SchemaRegistry:
    def __init__(self):
        base = Path(settings.SCHEMAS_DIR)
        self.schemas = {
            "r4010": xmlschema.XMLSchema(base / settings.XSD_R4010),
            "r4020": xmlschema.XMLSchema(base / settings.XSD_R4020),
        }

    def get(self, key: str) -> xmlschema.XMLSchema:
        return self.schemas[key]