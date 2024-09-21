# Job Crawler System 

This document provides a detailed explanation of the Job Crawler system, focusing on its design, architecture, functionality, and usage. It is intended for developers and engineers working on or maintaining the project.

## Table of Contents
<img align="right" width="200" src="banner.jpg">

1. [Introduction](#1-introduction)
2. [System Architecture](#2-system-architecture)
3. [Features](#3-features)
4. [File Structure](#4-file-structure)
5. [Installation and Setup](#5-installation-and-setup)
6. [Usage](#6-usage)
7. [Customization](#7-customization)
8.  [Future Enhancements](#8-future-enhancements)

## 1. Introduction
The Job Crawler system automates the job search process by:
- Extracting job listings from multiple platforms.
- Evaluating each job’s relevance to a candidate’s profile.
- Outputting structured JSON files for filtered and scored job data.

This documentation provides an overview of the system architecture, installation steps, and customization options.

## 2. System Architecture
The system is composed of three main components:
- **Scraping Engine**: Responsible for crawling job listings from platforms like TopCV, ITviec, and LinkedIn.
- **Relevancy Engine**: Uses an LLM to evaluate job suitability based on candidate profiles.
- **Storage & Output Module**: Saves the results in a structured format and provides logs for future reference.

**Architecture Diagram**:
> Consider adding a system architecture diagram here to show the flow of data between modules.

## 3. Features
The system scrapes job data from multiple platforms, processing raw information to extract key features like job `title`, `company`, and important metrics such as job `descriptions` and `requirements`. It then uses a large language model to evaluate the relevance of each job by comparing its description and requirements with the `candidate’s profile`. The output is a `relevancy` score that falls into one of four levels: High, Medium, Low, or Irrelevant, along with a rationale explaining why the job is relevant or irrelevant to the candidate.

Jobs marked as irrelevant are filtered out, ensuring that only relevant opportunities (those not labeled as `irrelevant`) are presented to the user. Meanwhile, all jobs, including their relevance scores and rationale, are stored in the system’s database. This process allows candidates to focus on jobs that are most aligned with their qualifications and preferences.

- **Multi-Platform Scraping**: Supports scraping from various platforms to gather a broad range of job opportunities.
- **AI-Powered Filtering**: Evaluates job relevance based on candidate profiles.
- **Structured Output**: Provides JSON files with relevancy scores and detailed job information.
- **Customizable**: Modify candidate profiles and filtering criteria as needed.
- **Efficient Automation**: Automates job search and evaluation, saving time for candidates.

## 4. File Structure
```
scripts/
├── data/
│   ├── filter/          (Filtered job data with relevancy != 'irrelevant')
│   ├── processed/       (Evaluate job data with relevancy scores)
│   └── raw/             (Raw job data scraped from sources)
├── scrapers/            (Scripts for scraping job postings)
│   ├── itviec.py        
│   ├── linkedin.py      
│   └── topcv.py         
├── scrape.py              (Main job scraper script)
├── filter.py              (Main job filter script)
├── upload.py              (Main job upload script)
├── script.sh              (Combined pipeline in bash script)
├── profile.json           (Candidate profile for evaluation)
```

## 5. Installation and Setup
### Prerequisites:
- Ensure Python 3.x and required packages (`bs4`, `requests`, `json`, `datetime`, `dotenv`, `langchain_openai`) are installed.
- Install required packages: 
```sh
pip install -r requirements.txt
```
- OpenAI API key (add to your `.env` file)

### Configuration:

- Set up your .env file with the OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```
- Customize the `profile.json` file with candidate-specific information.

## 6. Usage
All processes can be executed using the `script.sh`, details as follow

```sh
sh script.sh
```

### 1. Crawl Job Data:
Run `scripts/scrape.py`. This will scrape the specified job boards and save raw data to `data/raw/`.
### 2. Filtered and Scored Jobs:
Run `scripts/filter.py` and review the output files in `data/processed/`. Each file will contain jobs tailored to the candidate's profile, with a "relevancy" score indicating their relevance and a "reason" explaining their rationale.
### 3. Upload Jobs:
Run `scripts/upload.py` to upload the processed jobs to the database.

## 7. Customization
- Candidate Profile: Adjust `profile.json` to accurately reflect the candidate's information.
- Filtering Criteria: Modify the prompt within `JobMatchingAssistant` in `main.py` to refine how jobs are evaluated.
- Adding New Platforms: Expand the `scrapers/` directory with scripts to crawl more platforms.
- 
## 8. Future Enhancements
- [ ] UI Development: Add a front-end interface to simplify inputting candidate details and viewing job results.
- [x] Scheduler Integration: Implement a scheduling feature to automatically run the scraping process on a set interval (e.g., weekly).
- [x] Sorting Options: Add functionality to sort job listings by relevancy, date posted, or other factors.