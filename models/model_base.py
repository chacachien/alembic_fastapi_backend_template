from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from sqlmodel import Field, SQLModel, Relationship
import pytz
def get_default_datetime() -> datetime:
    # Get the current datetime in UTC timezone
    utc_now = datetime.now(pytz.utc)
    
    # Convert the datetime to Asia/Ho_Chi_Minh timezone
    ho_chi_minh_now = utc_now.astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))
    
    # Convert the timezone-aware datetime to naive datetime
    naive_now = ho_chi_minh_now.replace(tzinfo=None)
    
    return naive_now
class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=get_default_datetime,
        nullable=True,
    )
    updated_at: datetime = Field(
        default_factory=get_default_datetime,
        nullable=True,
        sa_column_kwargs={"onupdate": get_default_datetime},
    )
