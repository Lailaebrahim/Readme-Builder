import requests
import base64

def get_file_content(github_token, owner, repo, path, branch='main'):
  """Method to return content of a file based on it's path in repository 

  Args:
      github_token (str): user token 
      owner (str): username of owner of repo (case insensitive)
      repo (str): repository name
      path (str): path of file to get it's content
      branch (str, optional): Branch owned by user Defaults to 'main'.

  Returns:
      None : if path leads to a directory
      str : content of file if path leads to a file
      status code : if request was unsuccessful
  """
  
  headers = {
      'Accept': 'application/vnd.github+json',
      'Authorization': f'Bearer {github_token}',
      'X-GitHub-Api-Version': '2022-11-28'
  }
  
  # Get content of file
  url = f"https://api.github.com/repos/{
      owner}/{repo}/contents/{path}?ref={branch}"
  response = requests.get(url=url, headers=headers)
  if (response.status_code == 200):
      r = response.json()
      # if path leads to a directory response returns a list of objects inside the directory
      if isinstance(r, list):
          print(r)
          return None
      # if path leads to a file response return a dictionary with key content whose value is the actual content of file encoded in base64
      elif isinstance(r, dict):
          content = r.get('content')
          content = base64.b64decode(content).decode('utf-8')
          print(content)
          return content
  else:
      return response.status_code
  