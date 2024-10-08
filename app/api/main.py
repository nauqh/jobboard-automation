from fastapi import FastAPI, Depends, status, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import os
from .schemas import JobIn, JobBase

# Database
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

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


def get_password(request: Request):
    if not request.headers.get("password"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password required")

    return request.headers.get("password")


@app.post("/jobs", status_code=status.HTTP_201_CREATED)
async def add_jobs(data: List[JobIn], db: Session = Depends(get_db), password: str = Depends(get_password)):
    if password != os.environ["API_PWD"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    jobs = [models.Job(**job.model_dump()) for job in data]
    db.add_all(jobs)
    db.commit()

    return f"Added {len(jobs)} jobs"


@app.get("/jobs", response_model=List[JobBase])
def get_jobs(company: str = None, filtered: bool = False, tag: str = None,  db: Session = Depends(get_db)):
    """
    Get jobs from database.

    Args:
        \n- company (str, optional): Filter jobs by a specific company. Defaults to None.
        \n- filtered (bool, optional): Apply weekly suitability filtering. When `True`, only jobs uploaded in the current week and with a relevancy other than `irrelevant` are returned. Defaults to False.
        \n- tag (str, optional): Filter jobs by a specific tag. `fsw` or `data`. Defaults to None.

    Returns:
        \n- A list of job postings that match the specified filters, sorted by the upload date.
    """

    query = db.query(models.Job)

    if filtered:
        query = query.filter(
            func.date(models.Job.uploaded_at) == func.current_date(),
            models.Job.relevancy != "irrelevant"
        )
    if company:
        query = query.filter(models.Job.company == company)

    if tag:
        query = query.filter(models.Job.tag == tag)

    query = query.order_by(models.Job.uploaded_at.desc(
    ) if company or not filtered else models.Job.uploaded_at)

    submissions = query.all()

    return submissions
