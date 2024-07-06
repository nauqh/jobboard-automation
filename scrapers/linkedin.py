from bs4 import BeautifulSoup
import requests
import time
import json

url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Analyst&location=Vietnam&f_E=2"

attempts = 0
ids = []

while attempts < 3 and not ids:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = soup.find_all('li')
    for job in jobs:
        base_card = job.find('div', class_='base-search-card')
        ids.append(base_card.get('data-entity-urn').split(":")[3])
    attempts += 1

job_data = []
for id in ids:
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{id}"

    while True:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.find('h2').text
            company = soup.find(
                'a', class_='topcard__org-name-link').text.strip()
            logo = soup.find('img').get('data-delayed-url')

            job_url = soup.find('a', class_='topcard__link').get('href')
            location = soup.find(
                'span', class_='topcard__flavor topcard__flavor--bullet').text.strip().split(',')[0]
            descriptions = [item.text.strip() for item in soup.find(
                'div', class_='description__text').find_all('ul')[0].find_all('li')]
            requirements = [item.text.strip() for item in soup.find(
                'div', class_='description__text').find_all('ul')[1].find_all('li')]
            job_data.append({
                'title': title,
                'company': company,
                'logo': logo,
                'url': job_url,
                'location': location,
                'descriptions': descriptions,
                'requirements': requirements
            })
            break
        except Exception as e:
            print(f"{e}. Retrying...")
            time.sleep(2)


with open(f"data/raw/linkedin_jobs2.json", 'w', encoding='utf-8') as file:
    json.dump(job_data, file, ensure_ascii=False)
