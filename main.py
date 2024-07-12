import subprocess
import requests
import os
import json

# NOTE: CWD is /scripts


def run_script():
    try:
        os.chdir('scripts')
        subprocess.run(['sh', 'script.sh'],
                       check=True)
        print("Script completed successfully.")
    except subprocess.CalledProcessError as e:
        print("Script failed with error:", e)


def get_subfolder_names(path=None):
    if path is None:
        path = os.getcwd()

    return os.listdir(path)


# run_script()
URL = "http://127.0.0.1:8000"

for path in get_subfolder_names('scripts/data/processed/'):
    tag = 'data' if 'data' in path else 'fsw'
    with open(os.path.join('scripts/data/processed', path), 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            item['tag'] = tag
        response = requests.post(URL + "/jobs", json=data)
        print(response.text)
