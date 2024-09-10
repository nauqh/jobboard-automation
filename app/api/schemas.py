from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from datetime import datetime


class JobBase(BaseModel):
    title: str
    company: str
    logo: str
    url: str
    tag: str
    location: str
    relevancy: str
    reason: str
    uploaded_at: Optional[datetime] = None


class JobIn(JobBase):
    descriptions: list | str
    requirements: list | str
    uploaded_at: Optional[datetime] = None
