from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# Schemas
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Database
from . import models
from .database import engine, get_db

"""
DATABASE STATUS

Current storage: 198MB
Max storage: 5GB
"""

models.Base.metadata.create_all(bind=engine)


class JobBase(BaseModel):
    title: str
    company: str
    url: str
    suitability: int
    uploaded_at: Optional[datetime] = None


class JobIn(JobBase):
    title: str
    company: str
    logo: str
    url: str
    location: str
    descriptions: list
    requirements: list
    tag: str
    suitability: int
    uploaded_at: Optional[datetime] = None


app = FastAPI(
    title='Job Board Automation',
    summary="Storage for job crawlers",
    version='0.0.2'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return {"message": "Root endpoint"}


@app.post("/jobs", status_code=status.HTTP_201_CREATED)
def add_jobs(data: List[JobIn], db: Session = Depends(get_db)):
    """
    Post jobs to database.
    """
    jobs = [models.Job(**job.model_dump()) for job in data]
    db.add_all(jobs)
    db.commit()

    return f"Added {len(jobs)} jobs"


@app.get("/jobs", response_model=List[JobBase])
def get_jobs(company: str = None, filtered: bool = False,  db: Session = Depends(get_db)):
    """
    Get jobs from database.

    Query params:
        company (str, optional): Get jobs from a specific company. Defaults to None.
        filtered (bool, optional): Get jobs from the current week. Defaults to False.

    Returns:
        List[JobBase]: A list of jobs
    """

    if filtered:
        submissions = db.query(models.Job).filter(
            func.date_trunc('week', models.Job.uploaded_at) == func.date_trunc(
                'week', func.current_date())
        ).all()
    elif company:
        submissions = db.query(models.Job).filter(
            models.Job.company == company).order_by(models.Job.uploaded_at.desc()).all()
    else:
        submissions = db.query(models.Job).order_by(
            models.Job.uploaded_at.desc()).all()

    return submissions
