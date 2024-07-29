import requests
import json
import os
import sys

# Configuration
GITHUB_TOKEN = os.getenv('PAT_TOKEN')
ORGANIZATION = 'hmcts-test'
RULESET_NAME = 'Default Organization Ruleset'
REPO_FILE = 'production-repos.json'

if not GITHUB_TOKEN:
    print("Error: PAT_TOKEN not found in environment variables.")
    sys.exit(1)

# Headers for authentication
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
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

# Function to get the existing ruleset by name
def get_existing_ruleset(org, ruleset_name):
    url = f'https://api.github.com/orgs/{org}/rulesets'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    rulesets = response.json()
    for ruleset in rulesets:
        if ruleset['name'] == ruleset_name:
            return ruleset['id']
    return None

# Function to get the current ruleset by ID
def get_ruleset(org, ruleset_id):
    url = f'https://api.github.com/orgs/{org}/rulesets/{ruleset_id}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to create a new ruleset
def create_ruleset(org, data):
    url = f'https://api.github.com/orgs/{org}/rulesets'
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()

# Function to update the existing ruleset
def update_ruleset(org, ruleset_id, data):
    url = f'https://api.github.com/orgs/{org}/rulesets/{ruleset_id}'
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()

try:
    # Load repositories from JSON file
    target_repositories = load_repositories(REPO_FILE)
    print(f"Loaded repositories: {target_repositories}")

    # Check if the ruleset exists
    ruleset_id = get_existing_ruleset(ORGANIZATION, RULESET_NAME)
    if ruleset_id:
        # Get the current ruleset data
        ruleset = get_ruleset(ORGANIZATION, ruleset_id)
        print("Current Ruleset:")
        print(json.dumps(ruleset, indent=4))

        # Update the repository_name condition
        ruleset['conditions']['repository_name']['include'] = target_repositories

        # Update the ruleset on GitHub
        updated_ruleset = update_ruleset(ORGANIZATION, ruleset_id, ruleset)
        print("Updated Ruleset:")
        print(json.dumps(updated_ruleset, indent=4))
    else:
        # Create a new ruleset
        new_ruleset_data = {
            "name": RULESET_NAME,
            "target": "branch",
            "enforcement": "active",
            "conditions": {
                "ref_name": {
                    "include": ["refs/heads/main", "refs/heads/master"],
                    "exclude": []
                },
                "repository_name": {
                    "include": target_repositories,
                    "exclude": []
                }
            },
            "rules": [
                {
                    "type": "required_linear_history"
                },
                {
                    "type": "required_pull_request_reviews",
                    "parameters": {
                        "required_approving_review_count": 1,
                        "dismiss_stale_reviews": True,
                        "require_code_owner_reviews": False
                    }
                },
                {
                    "type": "required_status_checks",
                    "parameters": {
                        "strict": True,
                        "contexts": []  # Add specific status checks if needed
                    }
                }
            ]
        }
        print("Creating New Ruleset with data:")
        print(json.dumps(new_ruleset_data, indent=4))

        created_ruleset = create_ruleset(ORGANIZATION, new_ruleset_data)
        print("Created New Ruleset:")
        print(json.dumps(created_ruleset, indent=4))

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response content: {http_err.response.content.decode()}")
    sys.exit(1)
except Exception as err:
    print(f"An error occurred: {err}")
    sys.exit(1)
