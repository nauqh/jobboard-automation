# Job Matching Assistant

## Project Overview
This project is a job matching assistant designed to evaluate job descriptions for their suitability to a given candidate. It scrapes job listings from websites like **TopCV**, **ITviec** and **LinkedIn**, processes these listings, and then evaluates them against a candidate's profile to determine their relevance. The assistant uses criteria such as the candidate's years of experience and toolset proficiency to make its evaluations.

## File Structure

### Root Directory
- `.env`: Contains environment variables for the project.
- `.gitignore`: Specifies intentionally untracked files to ignore.
- `main.py`: The main script that orchestrates the scraping, processing, and evaluation of job listings.
- `README.md`: Provides an overview of the project and its structure.

### Data Directory
The `data/` directory is organized into two subdirectories: `raw/` and `processed/`.

#### Raw Data
- `data/raw/itviec_jobs.json`: Contains raw job listings scraped from ITviec.
- `data/raw/topcv_jobs.json`: Contains raw job listings scraped from TopCV.

#### Processed Data
- `data/processed/itviec_jobs_with_relevancy.json`: Contains processed ITviec job listings with relevancy scores added.
- `data/processed/jobs_with_relevancy.json`: Contains processed job listings from both ITviec and TopCV with relevancy scores added.

### Scrapers Directory
The `scrapers/` directory contains scripts used to scrape job listings from specific websites.
- `scrapers/itviec.py`: Scrapes job listings from ITviec.
- `scrapers/topcv.py`: Scrapes job listings from TopCV.

## How It Works
1. The scraping scripts in the `scrapers/` directory are used to collect job listings from ITviec and TopCV.
2. The `main.py` script processes these listings, evaluating each job's suitability for a given candidate profile based on years of experience and toolset proficiency.
3. The processed job listings, now with relevancy scores, are saved in the `data/processed/` directory.

## Setup and Execution
1. Ensure Python 3 and required packages (`bs4`, `urllib`, `json`, `datetime`, `dotenv`, `langchain_openai`, `langchain_core`) are installed.
2. Set up the `.env` file with necessary environment variables.
3. Run `main.py` to execute the job matching assistant.
