import json
import os
from scrapers.itviec import scrape_jobs
from scrapers.topcv import scrape_jobs_topcv

BASE = "data/raw2/"


def save_jobs_to_json(job_data, file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(job_data, file, ensure_ascii=False)


itviec_jobs_data = scrape_jobs("https://itviec.com/it-jobs/data-analyst-sql")
itviec_jobs_fsw = scrape_jobs("https://itviec.com/it-jobs/reactjs")

topcv_jobs_data = scrape_jobs_topcv(
    "https://www.topcv.vn/tim-viec-lam-data-analyst?exp=2")
topcv_jobs_fsw = scrape_jobs_topcv(
    "https://www.topcv.vn/tim-viec-lam-reactjs?exp=2")


save_jobs_to_json(itviec_jobs_data, BASE + "itviec_jobs_data.json")
save_jobs_to_json(itviec_jobs_fsw, BASE + "itviec_jobs_fsw.json")
save_jobs_to_json(topcv_jobs_data, BASE + "topcv_jobs_data.json")
save_jobs_to_json(topcv_jobs_fsw, BASE + "topcv_jobs_fsw.json")
