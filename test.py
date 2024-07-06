import json
import os
from scrapers.itviec import scrape_jobs

BASE = "data/raw/"


def save_jobs_to_json(job_data, file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(job_data, file, ensure_ascii=False)


itviec_jobs = scrape_jobs("https://itviec.com/it-jobs/data-analyst-sql")


save_jobs_to_json(itviec_jobs, BASE + "itviec_jobs.json")
