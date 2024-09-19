from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .cron import cron_job

app = FastAPI(
    title='Job Board Automation - Vercel Instance',
    summary="Cron job runner for job crawlers",
    version='0.0.3'
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
    return {"message": "Vercel instance - Cron job runner"}


@app.get("/api/cron")
async def run_cron_job():
    return cron_job()
