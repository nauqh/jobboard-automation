import subprocess
import os


def run_step(step: str, command: str):
    print(f"Starting {step}...")
    status = subprocess.run(command, shell=True).returncode

    if status == 0:
        print(f"{step} successful!")
        return True
    else:
        print(f"{step} failed.")
        return False


def main():
    os.chdir("scripts")
    if run_step("Scraping", "python scrape.py"):
        if run_step("Filtering", "python filter.py"):
            run_step("Uploading", "python upload.py")


if __name__ == "__main__":
    main()
