import os
import json

# File path for the JSON file
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), '../production-repos.json')
README_FILE_PATH = os.path.join(os.path.dirname(__file__), '../ReadMe.md')

def load_repos(file_path):
    """
    Load repositories from the given JSON file.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: '{file_path}' not found.")
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error reading {file_path}: {e}")
        raise

def update_readme(prod_count, dev_count):
    """
    Update the README file with the counts of various types of repositories.
    """
    with open(README_FILE_PATH, 'r') as file:
        readme_content = file.readlines()

    table_content = f"""
| **Repository Type**       | **Count** |
|---------------------------|-----------|
| Production Repositories   | {prod_count}        |
| Development Repositories  | {dev_count}        |
"""

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
            + [table_content]
            + readme_content[end_index:]
        )
    else:
        readme_content.append(f"\n{start_marker}\n{table_content}\n{end_marker}\n")

    with open(README_FILE_PATH, 'w') as file:
        file.writelines(readme_content)

# Load production repositories
try:
    production_repos = load_repos(JSON_FILE_PATH)
    production_count = len(production_repos)
    print(f"Number of production repositories: {production_count}")
    
    # Placeholder value for dev repo count, can be updated similarly
    development_count = 0  # Update this to load actual data if available
    
    update_readme(production_count, development_count)
except Exception as e:
    print(f"Failed to load or update repositories: {str(e)}")
