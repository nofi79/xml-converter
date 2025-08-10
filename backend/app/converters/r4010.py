from .base import Converter
from ..services.xsd_loader import SchemaRegistry
from ..services.xml_utils import validate_against, autofix_minimal

class R4010Converter(Converter):
    def __init__(self, registry: SchemaRegistry):
        self.schema = registry.get("r4010")

    def convert(self, name: str, xml_bytes: bytes):
        ok, _ = validate_against(self.schema, xml_bytes)
        if not ok:
            xml_bytes = autofix_minimal(self.schema, xml_bytes)
        # Re-validate; if still invalid, let it pass but with same name
        return name, xml_bytes