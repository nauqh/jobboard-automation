import json
import os

# Scrapers
from scrapers.itviec import scrape_jobs as scrape_itviec
from scrapers.topcv import scrape_jobs_topcv
from scrapers.linkedin import scrape_jobs_linkedin


class JobScraper:
    def __init__(self, base_path):
        self.base_path = base_path
        self.scrapers = {
            'itviec': scrape_itviec,
            'topcv': scrape_jobs_topcv,
            'linkedin': scrape_jobs_linkedin,
        }

    def save_jobs_to_json(self, job_data, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(job_data, file, ensure_ascii=False)

    def scrape_and_save(self, platform, url, file_name):
        if platform in self.scrapers:
            jobs_data = self.scrapers[platform](url)
            self.save_jobs_to_json(
                jobs_data, os.path.join(self.base_path, file_name))
            print(
                f"Scraped jobs from {platform.capitalize()} and saved to {file_name}")
        else:
            raise ValueError(f"Unsupported platform: {platform}")

    def load_json_files_from_folder(self, folder_path):
        data = []
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if file_name.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    data.extend(json.load(file))
        return data

    def combine_json_files(self, output_name, folder_name):
        folder_path = os.path.join(self.base_path, folder_name)
        data = self.load_json_files_from_folder(folder_path)
        output_path = os.path.join(self.base_path, output_name)
        with open(output_path, 'w', encoding='utf-8') as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=4)
        print(f"Combined JSON files into {output_name}")


if __name__ == "__main__":
    scraper = JobScraper("data/raw/")

    # ITViec Scraping
    scraper.scrape_and_save(
        'itviec', "https://itviec.com/it-jobs/data-analyst-sql", "DS/itviec_jobs_data.json")
    scraper.scrape_and_save(
        'itviec', "https://itviec.com/it-jobs/reactjs", "FSW/itviec_jobs_fsw.json")

    # TopCV Scraping
    scraper.scrape_and_save(
        'topcv', "https://www.topcv.vn/tim-viec-lam-data-analyst?exp=3", "DS/topcv_jobs_data.json")
    scraper.scrape_and_save(
        'topcv', "https://www.topcv.vn/tim-viec-lam-frontend-developer?exp=3", "FSW/topcv_jobs_fsw.json")

    # LinkedIn Scraping
    scraper.scrape_and_save(
        'linkedin', "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Analyst&location=Vietnam&f_E=2", "DS/linkedin_jobs_data.json")
    scraper.scrape_and_save(
        'linkedin', "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=React.js&location=Vietnam&f_TPR=&f_E=2", "FSW/linkedin_jobs_fsw.json")

    # Combine JSON files
    scraper.combine_json_files("ds_jobs.json", "DS")
    scraper.combine_json_files("fsw_jobs.json", "FSW")
