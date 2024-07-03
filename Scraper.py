import requests
from bs4 import BeautifulSoup
import csv

# URL of the website you want to scrape
URL = 'http://example.com/jobs'  # Replace with the actual URL of the job listings
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def get_job_listings():
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find job listings in the HTML (the specific tag and class will vary)
        jobs = soup.find_all('div', class_='job-listing')

        job_list = []

        for job in jobs:
            title = job.find('h2').text.strip()
            company = job.find('span', class_='company').text.strip()
            location = job.find('span', class_='location').text.strip()
            summary = job.find('p', class_='summary').text.strip()

            job_list.append({
                'Title': title,
                'Company': company,
                'Location': location,
                'Summary': summary
            })

        return job_list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return []

def save_to_csv(jobs):
    keys = jobs[0].keys()
    with open('job_listings.csv', 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(jobs)

if __name__ == "__main__":
    jobs = get_job_listings()
    if jobs:
        save_to_csv(jobs)
        print(f"Saved {len(jobs)} job listings to job_listings.csv")
    else:
        print("No job listings found.")
