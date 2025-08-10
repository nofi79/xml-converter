from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    SCHEMAS_DIR: str = os.getenv("SCHEMAS_DIR", "app/static_schemas")
    XSD_R4010: str = os.getenv("XSD_R4010", "R4010.xsd")
    XSD_R4020: str = os.getenv("XSD_R4020", "R4020.xsd")
    MAX_BATCH_SIZE: int = int(os.getenv("MAX_BATCH_SIZE", "50"))
    CORS_ORIGINS: list[str] = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]

settings = Settings()