from lxml import etree
from typing import Tuple
import xmlschema

NSMAP_CLEAN = None  # adjust if you need namespaces

def parse_xml_bytes(data: bytes) -> etree._ElementTree:
    parser = etree.XMLParser(remove_blank_text=True)
    return etree.fromstring(data, parser=parser)


def validate_against(schema: xmlschema.XMLSchema, xml_bytes: bytes) -> Tuple[bool, list[str]]:
    errors = []
    try:
        schema.validate(xml_bytes)
        return True, errors
    except xmlschema.validators.exceptions.XMLSchemaValidationError as e:
        # Collect readable errors
        for ve in schema.iter_errors(xml_bytes):
            errors.append(str(ve))
        return False, errors


def autofix_minimal(schema: xmlschema.XMLSchema, xml_bytes: bytes) -> bytes:
    """
    A minimal, safe auto-fix strategy:
    - Convert xml to dict via schema to reveal missing/invalid parts.
    - Fill missing required fields with schema defaults where available.
    - Re-serialize to XML following the schema.
    NOTE: tailor rules per R4010/R4020 in converter classes.
    """
    # xmlschema's to_dict will raise if invalid; use to_dict with validation='lax'
    data = schema.to_dict(xml_bytes, validation='lax')
    # Here you can inject defaults, e.g. required tags with fixed/default values
    # Example pattern (pseudo-rule):
    # if 'lote' not in data: data['lote'] = {}
    xml_obj = schema.encode(data)
    return xmlschema.etree_tostring(xml_obj, xml_declaration=True, encoding='utf-8')