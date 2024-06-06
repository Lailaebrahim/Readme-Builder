from github import Github
import config

def print_repo_tree(repo, path="", level=0, prefix=""):
    contents = repo.get_contents(path)
    contents.sort(key=lambda content: content.type)  
    for index, content in enumerate(contents):
        connector = "└── " if index == len(contents) - 1 else "├── "
        print(prefix + connector + content.name)
        if content.type == 'dir':
            extension = "    " if index == len(contents) - 1 else "│   "
            print_repo_tree(repo, content.path, level + 1, prefix + extension)

def main():
    g = Github(config.TOKEN)

    username = "Ahmed-Hereiz"
    repo_name = "hereiz-AI-terminal-assistant"

    repo = g.get_user(username).get_repo(repo_name)

    print_repo_tree(repo)

if __name__ == "__main__":
    main()
