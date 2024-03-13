import pandas as pd


job_df = pd.read_csv("linkedin_job_post.csv")

print(job_df['job id'].nunique())