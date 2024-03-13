import requests
from bs4 import BeautifulSoup
import math
import pandas as pd
import json
import time


# canada_job_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data%20scientist%20jobs&location=Canada&start={}'


keyword = "UN%2Bjobs"
location = "United%2BStates"
# job_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=UN%2Bjobs&location=United%2BStates&currentJobId=3853050939&start={}"

job_url = "https://www.linkedin.com/jobs/search?keywords=Anesthesiologist&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum={}"

# job_url = "https://www.linkedin.com/jobs/search/?currentJobId=3856235249&start={}"

# https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%2BScience&location=canada&geoId=&trk=public_jobs_jobs-search-bar_search-submit&start=25

# Change start and end value as required, this means the pages of linkedin job search

# try only 1000 at a time, you may get connection error, change start and end accordingly, per_page is 25 incase of linkedin

# -- What I noticed is it gives 400 (bad request) for start >= 1000, so we can change the keywords after every 1000
start = 0
end = 26
per_page=1


job_id_list = list()

for i in range(start, end, per_page):
    status_code = 429
    print(i)
    if i>0 and i%500 == 0:
        with open('job_ids.json', 'w') as f:
            json.dump(job_id_list, f)   
        # sleep for 1 mins after every 500th i        
        time.sleep(60)
        
    while status_code == 429:
        res = requests.get(job_url.format(i))
        status_code = res.status_code
        print(res.status_code)
        soup=BeautifulSoup(res.text,'html.parser')
        alljobs_on_this_page=soup.find_all("li")

        # print(alljobs_on_this_page)

        for x in range(0,len(alljobs_on_this_page)):
            jobid_element = alljobs_on_this_page[x].find("div",{"class":"base-card"})
            if jobid_element is not None:
                jobid = jobid_element.get('data-entity-urn')
                if jobid is not None:
                    jobid = jobid.split(":")[3]
                    job_id_list.append(jobid)
                else:
                    print("Job ID not found")
            
            # jobid = alljobs_on_this_page[x].find("div",{"class":"base-card"}).get('data-entity-urn').split(":")[3]
            # job_id_list.append(jobid)

    print(job_id_list)
    
    

with open('job_ids.json', 'w') as f:
    json.dump(job_id_list, f)