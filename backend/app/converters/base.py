from abc import ABC, abstractmethod
from typing import Tuple

class Converter(ABC):
    @abstractmethod
    def convert(self, name: str, xml_bytes: bytes) -> Tuple[str, bytes]:
        """Return (new_name, converted_xml_bytes)."""
        raise NotImplementedError