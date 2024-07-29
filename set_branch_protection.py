import requests
import json
import os
import sys

# Configuration
GITHUB_TOKEN = os.getenv('PAT_TOKEN')
ORGANIZATION = 'hmcts-test'
BRANCH_NAME = 'master'
REPO_FILE = 'production-repos.json'

if not GITHUB_TOKEN:
    print("Error: PAT_TOKEN not found in environment variables.")
    sys.exit(1)

# Headers for authentication
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Function to load repositories from JSON file
def load_repositories(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        if isinstance(data, list):
            return data
        else:
            raise ValueError("Unexpected JSON format. Expected a list of repositories.")

# Function to update branch protection rules
def update_branch_protection(org, repo, branch):
    url = f'https://api.github.com/repos/{org}/{repo}/branches/{branch}/protection'
    protection_settings = {
        "required_status_checks": {
            "strict": True,
            "contexts": []
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": True,
            "required_approving_review_count": 1
        },
        "restrictions": None
    }
    
    response = requests.put(url, headers=headers, data=json.dumps(protection_settings))
    response.raise_for_status()
    return response.json()

try:
    # Load repositories from JSON file
    target_repositories = load_repositories(REPO_FILE)
    print(f"Loaded repositories: {target_repositories}")

    for repo in target_repositories:
        print(f"Updating branch protection for {repo}/{BRANCH_NAME}")
        result = update_branch_protection(ORGANIZATION, repo, BRANCH_NAME)
        print(f"Updated branch protection for {repo}/{BRANCH_NAME}:")
        print(json.dumps(result, indent=4))

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response content: {http_err.response.content.decode()}")
    sys.exit(1)
except Exception as err:
    print(f"An error occurred: {err}")
    sys.exit(1)
