from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import json


url = "https://itviec.com/it-jobs/data-analyst-sql"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}


page = urlopen(Request(url, headers=headers))
soup = BeautifulSoup(page, "html.parser")
jobs = soup.find_all('div', class_='ipy-2')

job_data = []
for job in jobs:
    job_url = "https://itviec.com/" + job.find('a')['href']
    title = job.find('h3').text.strip()

    if any(keyword in title.lower() for keyword in ['senior', 'manager', 'leader', 'sr.']):
        continue

    company = job.find(
        'div', class_='imy-3 d-flex align-items-center').span.text.strip()
    logo = job.find(
        'div', class_='imy-3 d-flex align-items-center').a.img['data-src']

    mode, location = [div.span.text.strip()
                      for div in job.find_all('div',
                                              class_='d-flex align-items-center text-dark-grey imt-1')]

    tags = ' '.join([f'`{a.text.strip()}`' for a in job.find(
        'div', class_='imt-3 imb-2').find_all('a')])

    page = urlopen(Request(job_url, headers=headers))
    soup = BeautifulSoup(page, "html.parser")
    job_description = soup.find_all('div', class_='imy-5 paragraph')[0]
    job_requirement = soup.find_all('div', class_='imy-5 paragraph')[1]

    # Handle different types of list items (Some pages have ul and li, some pages have p)
    descriptions = "\n".join([
        f"- {li.get_text(strip=True)}"
        for ul in job_description.find_all("ul")
        for li in ul.find_all("li")
    ])
    descriptions += "\n".join([
        f"- {p.get_text(strip=True)}"
        for p in job_description.find_all("p")
    ])

    requirements = "\n".join([
        f"- {li.get_text(strip=True)}"
        for ul in job_requirement.find_all("ul")
        for li in ul.find_all("li")
    ])
    requirements += "\n".join([
        f"- {p.get_text(strip=True)}"
        for p in job_requirement.find_all("p")
    ])

    job_data.append({
        'title': title,
        'company': company,
        'logo': logo,
        'url': job_url,
        'location': location,
        'mode': mode,
        'descriptions': descriptions,
        'requirements': requirements
    })

with open(f"data/raw/itviec_jobs.json", 'w', encoding='utf-8') as file:
    json.dump(job_data, file, ensure_ascii=False)
