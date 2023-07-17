import base64
import requests

def get_github_files_and_contents(github_url):
    api_url = github_url.replace('github.com', 'api.github.com/repos', 1) + '/contents/'
    headers = {'Accept': 'application/vnd.github.v3.raw'}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an exception if the response was not 200 OK
    except requests.exceptions.HTTPError as err:
        print(f'HTTP error occurred: {err}')  # Print the HTTP error if one occurred
    except requests.exceptions.RequestException as err:
        print(f'Request error occurred: {err}')  # Print the request error if one occurred
    else:
        file_data = response.json()  # If the request was successful, parse the response as JSON
        print(file_data)
        for file in file_data:
            if file['type'] == 'file':
                print(f"\nFile Name: {file['name']}")
                content = requests.get(file['download_url'], headers=headers).content
                print(f"Content: {content.decode('utf-8')}")
            else:
                print(f"{file['name']} is a directory")

def validate_url(url: str):
    # should match something like https://github.com/chasemc67/TinyGen
    # specifically the url github.com, followed by username and repo, with no trailing slash
    pattern = r'^https://github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+$'
    if re.match(pattern, url):
        return True
    else:
        return False


# Example usage:
# get_github_files_and_contents('https://github.com/chasemc67/TinyGen')