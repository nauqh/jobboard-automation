import subprocess
import os


def run_script():
    try:
        os.chdir('scripts')
        subprocess.run(['sh', 'script.sh'],
                       check=True)
        print("Script completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Script failed with error:", e)


run_script()
