import requests
from create_tree import create_tree


def get_repo_tree(github_token, owner, repo, branch='main'):
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {github_token}',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    # Get languages of a repo
    url = f'https://api.github.com/repos/{owner}/{repo}/languages'
    response = requests.get(url=url, headers=headers)

    if (response.status_code == 200):
        if response.json().items():
            repo_tree = "The programming languages used in repository and the number of bytes of code written in each language.\n"
            for key, value in response.json().items():
                repo_tree += f"{key}: {value}\n"
        else:
            repo_tree = """"""
    else:
        return response.status_code

    # Get the sha of the repository and check if it exists
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}"
    response = requests.get(url=url, headers=headers)
    if (response.status_code == 200):
        tree_sha = response.json().get('sha')
        
        #Get the tree of repository recursively 
        url = f'https://api.github.com/repos/{owner}/{
            repo}/git/trees/{tree_sha}?recursive=true'    
        response = requests.get(url=url, headers=headers)
        
        if (response.status_code == 200):
            repo_tree += "The tree of repository:\n"
            tree_list = response.json().get('tree')
            tree_str = """"""
            for item in tree_list:
                tree_str += str(item.get('path')) + '\n'
            repo_tree += create_tree(tree_str)
            return repo_tree
        
        else:
            return response.status_code
        
    else:
        return response.status_code
