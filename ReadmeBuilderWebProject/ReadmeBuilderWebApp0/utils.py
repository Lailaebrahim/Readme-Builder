import requests


def is_valid_github_username(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        return None
