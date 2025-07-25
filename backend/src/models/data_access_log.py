from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class DataAccessLog(BaseModel):
    id: str = Field(description="Unique log identifier")
    user_id: str = Field(description="Firebase user ID")
    action: str = Field(description="Action performed (read, write, delete, etc.)")
    resource_type: str = Field(description="Type of resource accessed")
    resource_id: str = Field(description="ID of the accessed resource")
    ip_address: Optional[str] = Field(
        default=None, description="IP address of the request"
    )
    user_agent: Optional[str] = Field(default=None, description="User agent string")
    success: bool = Field(description="Whether the action was successful")
    error_message: Optional[str] = Field(
        default=None, description="Error message if failed"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Access timestamp"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional log metadata"
    )
