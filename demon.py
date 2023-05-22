import os

from pylib.testcaseLib import run, get_oldest_job


while True:
    job = get_oldest_job()
    if job:
        run(job)
        os.remove(f"jobs/{job}")
