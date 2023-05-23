import os
import time

from pylib.testcaseLib import run_test, get_oldest_job, get_job_details


while True:
    job = get_oldest_job()
    time.sleep(2)
    if job:
        job_details = get_job_details(".", job)
        run_test(job_details["build"][0], job_details["env"][0], job_details["suite"][0])
        os.remove(f"jobs/{job}")
