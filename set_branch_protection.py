import requests
import json
import os

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ORGANIZATION = 'hmcts-test'
RULESET_ID = '1239224'
REPO_FILE = 'production-repos.json'

# Headers for authentication
headers = {
    'Authorization': f'Bearer {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json',
    'Content-Type': 'application/json'
}

# Function to load repositories from JSON file
def load_repositories(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        if isinstance(data, list):
            return data
        else:
            raise ValueError("Unexpected JSON format. Expected a list of repositories.")

# Function to get the current ruleset
def get_ruleset(org, ruleset_id):
    url = f'https://api.github.com/orgs/{org}/rulesets/{ruleset_id}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to update the ruleset
def update_ruleset(org, ruleset_id, data):
    url = f'https://api.github.com/orgs/{org}/rulesets/{ruleset_id}'
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()

try:
    # Load repositories from JSON file
    target_repositories = load_repositories(REPO_FILE)
    print(f"Loaded repositories: {target_repositories}")

    # Get the current ruleset data
    ruleset = get_ruleset(ORGANIZATION, RULESET_ID)
    print("Current Ruleset:")
    print(json.dumps(ruleset, indent=4))

    # Update the repository_name condition
    ruleset['conditions']['repository_name']['include'] = target_repositories

    # Update the ruleset on GitHub
    updated_ruleset = update_ruleset(ORGANIZATION, RULESET_ID, ruleset)

    print("Updated Ruleset:")
    print(json.dumps(updated_ruleset, indent=4))

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
