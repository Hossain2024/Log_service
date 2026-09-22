from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class LogCreate(BaseModel):
    log_id: str = Field(min_length=1, max_length=100)
    service_name: str = Field(min_length=1, max_length=100)
    level: LogLevel
    message: str = Field(min_length=1, max_length=1000)
    timestamp: datetime


class LogResponse(LogCreate):
    model_config = ConfigDict(from_attributes=True)

