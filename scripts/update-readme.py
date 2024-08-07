import os
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# File path for the JSON file
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), '../production-repos.json')
README_FILE_PATH = os.path.join(os.path.dirname(__file__), '../readme.md')  # Ensure correct case

def load_repos(file_path):
    """
    Load repositories from the given JSON file.
    """
    try:
        with open(file_path, 'r') as f:
            repos = json.load(f)
            if not isinstance(repos, list):
                raise ValueError("JSON content is not a list")
            return repos
    except FileNotFoundError:
        logging.error(f"Error: '{file_path}' not found.")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error reading {file_path}: {e}")
        raise

def update_readme(prod_count, dev_count, prod_link):
    """
    Update the README file with the counts of various types of repositories.
    """
    try:
        with open(README_FILE_PATH, 'r') as file:
            readme_content = file.readlines()

        table_content = f"""
| **Repository Type**       | **Count** |
|---------------------------|-----------|
| Production Repositories   | [{prod_count}]({prod_link})        |
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
    except Exception as e:
        logging.error(f"Failed to update README file: {str(e)}")
        raise

# Load production repositories
try:
    production_repos = load_repos(JSON_FILE_PATH)
    production_count = len(production_repos)
    logging.info(f"Number of production repositories: {production_count}")
    
    # Placeholder value for dev repo count, can be updated similarly
    development_count = 0  # Update this to load actual data if available
    
    # Link to the production-repos.json file in the repository
    prod_link = "https://github.com/hmcts/github-repository-rules/blob/DTSPO-18104-typo-file-V2/production-repos.json"
    
    update_readme(production_count, development_count, prod_link)
except Exception as e:
    logging.error(f"Failed to load or update repositories: {str(e)}")