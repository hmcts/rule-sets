import os
import json

# File path for the JSON file
JSON_FILE_PATH = '../production-repos.json'
README_FILE_PATH = '../README.md'

def load_production_repos():
    """
    Load production repositories from production-repos.json file.
    """
    try:
        with open(JSON_FILE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: 'production-repos.json' not found at {os.path.abspath(JSON_FILE_PATH)}")
        print("Current working directory:", os.getcwd())
        print("Contents of the current directory:")
        print(os.listdir('.'))
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {JSON_FILE_PATH}: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error reading {JSON_FILE_PATH}: {e}")
        raise

def update_readme(repo_count):
    """
    Update the README file with the count of production repositories.
    """
    with open(README_FILE_PATH, 'r') as file:
        readme_content = file.readlines()

    new_line = f"\n**Production Repositories Count:** There are currently **{repo_count}** repositories marked as in production.\n"
    start_marker = "<!--START_PRODUCTION_COUNT-->"
    end_marker = "<!--END_PRODUCTION_COUNT-->"

    start_index = None
    end_index = None

    for i, line in enumerate(readme_content):
        if start_marker in line:
            start_index = i
        if end_marker in line:
            end_index = i

    if start_index is not None and end_index is not None:
        readme_content = (
            readme_content[:start_index + 1]
            + [new_line]
            + readme_content[end_index:]
        )
    else:
        readme_content.append(f"\n{start_marker}\n{new_line}\n{end_marker}\n")

    with open(README_FILE_PATH, 'w') as file:
        file.writelines(readme_content)

# Load production repositories
try:
    production_repos = load_production_repos()
    repo_count = len(production_repos)
    print(f"Number of production repositories: {repo_count}")
    update_readme(repo_count)
except Exception as e:
    print(f"Failed to load or update repositories: {str(e)}")
