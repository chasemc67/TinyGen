import requests
from dataclasses import dataclass
from typing import List
import re
import pickle
from fastapi import HTTPException

@dataclass
class GithubFile:
    filename: str
    content: str

def validate_url(url: str):
    # should match something like https://github.com/chasemc67/TinyGen
    # specifically the url github.com, followed by username and repo, with no trailing slash
    pattern = r'^https://github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$'
    if re.match(pattern, url):
        return True
    else:
        return False

def get_github_files_and_contents(github_url: str) -> List[GithubFile]:
    if not validate_url(github_url):
        raise Exception("Invalid Github URL")

    api_url = github_url.replace('github.com', 'api.github.com/repos', 1) + '/contents/'
    headers = {'Accept': 'application/vnd.github.v3.raw'}

    files = []

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an exception if the response was not 200 OK
    except requests.exceptions.HTTPError as err:
        raise HTTPException(status_code=500, detail=f'HTTP error occurred: {err}')
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=500, detail=f'Request error occurred: {err}')
    else:
        file_data = response.json()
        for file in file_data:
            if file['type'] == 'file':
                content = requests.get(file['download_url'], headers=headers).content.decode('utf-8')
                files.append(GithubFile(filename=file['name'], content=content))

    return files  # Return the list of GithubFile objects

# Read and write data which can be used for local testing instead of always hitting github API
def write_GithubFile_list_to_file(github_files: List[GithubFile]) -> None:
    with open('github_mock_data', 'wb') as f:
        pickle.dump(github_files, f)

def read_GithubFile_list_from_file() -> List[GithubFile]:
    with open('github_mock_data', 'rb') as f:
        github_files = pickle.load(f)
    return github_files