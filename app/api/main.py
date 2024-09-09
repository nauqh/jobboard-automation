from fastapi import FastAPI, Depends, status, HTTPException, Request
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import subprocess
from datetime import datetime, timedelta

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
    tag: str
    suitability: int
    uploaded_at: Optional[datetime] = None


class JobIn(JobBase):
    title: str
    company: str
    logo: str
    url: str
    location: str
    descriptions: list | str
    requirements: list | str
    suitability: int
    uploaded_at: Optional[datetime] = None


class JobOut(JobBase):
    title: str
    company: str
    logo: str
    url: str
    location: str
    suitability: int
    uploaded_at: Optional[datetime] = None


def run_step(step: str, command: str):
    print(f"Starting {step}...")
    status = subprocess.run(command, shell=True).returncode

    if status == 0:
        print(f"{step} successful!")
        return True
    else:
        print(f"{step} failed.")
        return False


def run_script():
    os.chdir("scripts")
    if run_step("Scraping", "python scrape.py"):
        if run_step("Filtering", "python filter.py"):
            run_step("Uploading", "python upload.py")


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(func=run_script, trigger='date',
    #                   run_date=datetime.now() + timedelta(seconds=3))
    scheduler.add_job(
        run_script, 'cron', day_of_week='mon', hour=8)
    scheduler.start()
    yield


app = FastAPI(
    title='Job Board Automation',
    summary="Storage for job crawlers",
    version='0.0.2',
    lifespan=lifespan
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
    if password != os.environ["PATH_PWD"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    jobs = [models.Job(**job.model_dump()) for job in data]
    db.add_all(jobs)
    db.commit()

    return f"Added {len(jobs)} jobs"


@app.get("/jobs", response_model=List[JobOut])
def get_jobs(company: str = None, filtered: bool = False, tag: str = None,  db: Session = Depends(get_db)):
    """
    Get jobs from database.

    Args:
        \n- company (str, optional): Filter jobs by a specific company. Defaults to None.
        \n- filtered (bool, optional): Apply weekly suitability filtering. When `True`, only jobs uploaded in the current week and with a suitability of 50 or higher are returned. Defaults to False.
        \n- tag (str, optional): Filter jobs by a specific tag. `fsw` or `data`. Defaults to None.

    Returns:
        \n- A list of job postings that match the specified filters, sorted by the upload date.
    """

    query = db.query(models.Job)

    if filtered:
        query = query.filter(
            func.date(models.Job.uploaded_at) == func.current_date(),
            models.Job.suitability >= 50
        )
    if company:
        query = query.filter(models.Job.company == company)

    if tag:
        query = query.filter(models.Job.tag == tag)

    query = query.order_by(models.Job.uploaded_at.desc(
    ) if company or not filtered else models.Job.uploaded_at)

    submissions = query.all()

    return submissions
