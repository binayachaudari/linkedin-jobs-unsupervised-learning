import requests
from bs4 import BeautifulSoup
import math
import pandas as pd
import json
import time

# fetch the job_ids that were scrapped from main.py
with open('job_ids.json', 'r') as f:
    job_id_list = json.load(f)

print("Total job ids: ", len(job_id_list))

print("Unique ids: ", len(set(job_id_list)))


individual_job_url = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'

# Create an empty list to store the data dictionaries
data = []
# Define the file path for the csv file
csv_file_path = 'linkedin_job_post.csv'

for i, job_id in enumerate(set(job_id_list)):
    
    if i>0 and i%100 == 0:
        df = pd.DataFrame(data)
        df.to_csv(csv_file_path, index=False, mode='a', header=False)
        print("Exported to CSV")
        # Create an empty list to store the data dictionaries
        data = []
        time.sleep(60) # if you know the throttle time of site, change it
        
    print(f"For id: {i} & job id : {job_id} ")
    status_code = 429
    while status_code == 429:
        # sleep for 2 sec before another request
        time.sleep(2)
        res = requests.get(individual_job_url.format(job_id))
        status_code = res.status_code

        soup=BeautifulSoup(res.text,'html.parser')
        # print(soup)
        # fetch the required values if status is 200
        if status_code == 200:
            print("status: ", status_code)
            job_title = soup.find("h2", {"class": "top-card-layout__title"})
            company_name = soup.find("a", {"class": "topcard__org-name-link"})
            company_location = soup.find("span", {"class" :"topcard__flavor topcard__flavor--bullet"}) 
            posted_time = soup.find("span", {"class": "posted-time-ago__text"})
            description = soup.find("div", {"class": "description__text"}).find('section').find('div')
            data_dict = {
                "job id": job_id,
                "job_title" : job_title.text.strip(),
                "company_name": company_name.text.strip(),
                "company_location": company_location.text.strip(),
                "posted_time": posted_time.text.strip(),
                "description": description.text.strip(),
            }
            # print(data_dict)
            data.append(data_dict)

# Atlast add to csv, it will add the the rows  after the loop is over
df = pd.DataFrame(data)
df.to_csv(csv_file_path, index=False, mode='a', header=False)
print("Final Export to CSV Completed")
