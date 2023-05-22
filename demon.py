import os

from pylib.testcaseLib import run, get_oldest_job, get_job_details


while True:
    job = get_oldest_job()
    if job:
        job_details = get_job_details(".", job)
        run(job_details)
        os.remove(f"jobs/{job}")
