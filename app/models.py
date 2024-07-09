from sqlalchemy import Column, Integer, String, DateTime, JSON, UniqueConstraint
from sqlalchemy.sql import func
from .database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String)
    company = Column(String)
    logo = Column(String)
    url = Column(String)
    location = Column(String)
    descriptions = Column(JSON)
    requirements = Column(JSON)

    tag = Column(String)
    suitability = Column(Integer)
    uploaded_at = Column(DateTime(timezone=True),
                         server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('title', 'company', name='_title_company_uc'),
    )
