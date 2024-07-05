import requests
import json
import base64


def push_readme(github_token, owner, repo, readme_content, branch='main'):
    """Method to return content of a file based on it's path in repository

  Args:
      github_token (str): user token
      owner (str): username of owner of repo (case insensitive)
      repo (str): repository name
      content (str): content of readme file to be pushed
      branch (str, optional): Branch owned by user Defaults to 'main'.

  Returns:
      status code : if request was unsuccessful
  """
    # Create the API endpoint URL
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/README.md"

    # Create the headers with the GitHub token and content type
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json",
        'X-GitHub-Api-Version': '2022-11-28'
    }

    # Convert the content from string to Base64-encoded representation of the original string.
    readme_content = (base64.b64encode(readme_content.encode('utf-8'))).decode('utf-8')
    
    # Check if the README.md already exists
    check_response = requests.get(url, headers=headers)

    # if file exists, get it's sha and send it with the payload to update instead of create
    if (check_response.status_code == 200):
        readme_sha = check_response.json().get('sha')
        payload = {
            "message": "Push README file from Readme Builder",
            "content": readme_content,
            "branch": branch,
            "sha": readme_sha
        }
    elif (check_response.status_code == 404):
        payload = {
            "message": "Push README file from Readme Builder",
            "content": readme_content,
            "branch": branch,
        }
    else:
        return (check_response.status_code)

    # Convert the payload to JSON
    payload_json = json.dumps(payload)

    # Make the PUT request to the API endpoint to create file if not exist or update if exist
    response = requests.put(url, headers=headers, data=payload_json)
    
    """retrun from PUT request 200 if updated successfully , 201 if created successfully
       404 if branch not found or repo , 409 if not authorized to update/create readme """
    return (response.status_code)