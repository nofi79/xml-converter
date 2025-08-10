from .base import Converter
from ..services.xsd_loader import SchemaRegistry
from ..services.xml_utils import validate_against, autofix_minimal

class R4020Converter(Converter):
    def __init__(self, registry: SchemaRegistry):
        self.schema = registry.get("r4020")

    def convert(self, name: str, xml_bytes: bytes):
        ok, _ = validate_against(self.schema, xml_bytes)
        if not ok:
            xml_bytes = autofix_minimal(self.schema, xml_bytes)
        return name, xml_bytes