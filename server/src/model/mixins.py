from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class TimeMixin(BaseModel):
    created_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )