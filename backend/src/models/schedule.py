from datetime import datetime
from enum import Enum
from typing import Any, Dict

from pydantic import BaseModel, Field


class ScheduleFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class ScheduleType(str, Enum):
    REMINDER = "reminder"
    REPORT = "report"
    ALERT = "alert"


class Schedule(BaseModel):
    id: str = Field(description="Unique schedule identifier")
    user_id: str = Field(description="Firebase user ID")
    title: str = Field(description="Schedule title")
    description: str = Field(default="", description="Schedule description")
    schedule_type: ScheduleType = Field(
        description="Type of schedule (reminder, report, alert)"
    )
    frequency: ScheduleFrequency = Field(
        description="Frequency (daily, weekly, monthly, custom)"
    )
    next_run: datetime = Field(description="Next scheduled run time")
    is_active: bool = Field(default=True, description="Whether schedule is active")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional schedule metadata"
    )
