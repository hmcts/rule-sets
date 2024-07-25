import requests
import json
import os

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ORGANIZATION = 'hmcts-test'
RULESET_ID = '1239224'
REPO_FILE = '../production_repos.json'  # Path to your JSON file

# Headers for authentication
headers = {
    'Authorization': f'Bearer {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json',
    'Content-Type': 'application/json'
}

# Function to load repositories from JSON file
def load_repositories(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        # Check if data is a list
        if isinstance(data, list):
            return data
        else:
            raise ValueError("JSON data should be a list of repositories")
    except Exception as e:
        print(f"Error loading repositories from {file_path}: {e}")
        raise

# Function to get the current ruleset
def get_ruleset(org, ruleset_id):
    url = f'https://api.github.com/orgs/{org}/rulesets/{ruleset_id}'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ruleset: {e}")
        raise

# Function to update the ruleset
def update_ruleset(org, ruleset_id, data):
    url = f'https://api.github.com/orgs/{org}/rulesets/{ruleset_id}'
    try:
        response = requests.patch(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error updating ruleset: {e}")
        raise

# Main logic
try:
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

except Exception as e:
    print(f"An error occurred: {e}")
