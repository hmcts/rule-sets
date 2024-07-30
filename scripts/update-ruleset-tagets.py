import requests
import json
import os

# Configuration
OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
ORGANIZATION = 'hmcts-test'
RULESET_ID = '1239224'
REPO_FILE = 'scripts/production_repos.json'

# Headers for authentication
headers = {
    'Authorization': f'Bearer {OAUTH_TOKEN}',
    'Accept': 'application/vnd.github+json',
    'Content-Type': 'application/json'
}

# Function to load repositories from JSON file
def load_repositories(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['repositories']

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

# Load repositories from JSON file
target_repositories = load_repositories(REPO_FILE)

# Get the current ruleset data
ruleset = get_ruleset(ORGANIZATION, RULESET_ID)

# Update the repository_name condition
ruleset['conditions']['repository_name']['include'] = target_repositories

# Update the ruleset on GitHub
updated_ruleset = update_ruleset(ORGANIZATION, RULESET_ID, ruleset)

print("Updated Ruleset:")
print(json.dumps(updated_ruleset, indent=4))
