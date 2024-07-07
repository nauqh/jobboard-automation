from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# Schemas
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Database
from . import models
from .database import engine, get_db

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
    suitability: int
    uploaded_at: Optional[datetime] = None


app = FastAPI(
    title='Job Board Automation',
    summary="Storage for jobs",
    version='0.0.1'
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


@app.post("/jobs", status_code=status.HTTP_201_CREATED, response_model=JobBase)
def create_note(data: JobIn, db: Session = Depends(get_db)):
    job = models.Job(**data.model_dump())

    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@app.get("/jobs")
def get_jobs_by_company(company: str, db: Session = Depends(get_db)):
    submissions = db.query(models.Job).filter(
        models.Job.company == company).order_by(models.Job.uploaded_at.desc()).all()

    return submissions
