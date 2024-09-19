import os
import subprocess


def run_step(step: str, command: str):
    print(f"Starting {step}...")
    status = subprocess.run(command, shell=True).returncode

    if status == 0:
        print(f"{step} successful!")
        return True
    else:
        print(f"{step} failed.")
        return False


def run_script():
    os.chdir("scripts")
    if run_step("Scraping", "python scrape.py"):
        if run_step("Filtering", "python filter.py"):
            run_step("Uploading", "python upload.py")


def cron_job():
    run_script()
    return {"message": "Cron job executed successfully"}
