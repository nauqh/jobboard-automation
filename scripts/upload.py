import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()


def get_subfolder_names(path=None):
    if path is None:
        path = os.getcwd()

    return os.listdir(path)


if __name__ == "__main__":
    # NOTE: Upload jobs
    URL = "https://jobboard.up.railway.app"

    for path in get_subfolder_names('data/processed/'):
        tag = 'data' if 'ds' in path else 'fsw'
        with open(os.path.join('data/processed/', path), 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                item['tag'] = tag
                item['suitability'] = 60 if item['relevancy'] != 'irrelevant' else 20
            headers = {
                'password': os.environ['API_PWD'],
                'Content-Type': 'application/json'
            }
            response = requests.post(URL + "/jobs", json=data, headers=headers)
            print(response.text)
