import requests
import os
import sys
import json

# GitHub organization name
ORG_NAME = "hmcts-test"

# GitHub PAT Token
GITHUB_TOKEN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("PAT_TOKEN")

if not GITHUB_TOKEN:
    print("Error: PAT_TOKEN not found in environment variables or command line arguments")
    sys.exit(1)

# Print masked token for debugging
print(f"Using token: {GITHUB_TOKEN[:4]}...{GITHUB_TOKEN[-4:]}")

# Headers for GitHub API requests
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "Content-Type": "application/json"
}

def load_repositories(file_path):
    """Read repositories from production-repos.json file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data['repositories']
    except FileNotFoundError:
        print("Error: production-repos.json file not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in production-repos.json")
        sys.exit(1)

def get_existing_ruleset(name):
    url = f"https://api.github.com/orgs/{ORG_NAME}/rulesets"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        rulesets = response.json()
        for ruleset in rulesets:
            if ruleset['name'] == name:
                return ruleset['id']
    return None

def get_ruleset(org, ruleset_id):
    url = f'https://api.github.com/orgs/{org}/rulesets/{ruleset_id}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def create_or_update_org_ruleset(repos):
    """Create or update an organization-level ruleset and assign repositories to it using REST API."""
    ruleset_name = "Default Organization Ruleset"
    existing_ruleset_id = get_existing_ruleset(ruleset_name)
    
    if existing_ruleset_id:
        ruleset = get_ruleset(ORG_NAME, existing_ruleset_id)
        ruleset["conditions"]["repository_name"]["include"] = repos
        url = f"https://api.github.com/orgs/{ORG_NAME}/rulesets/{existing_ruleset_id}"
        method = requests.patch
        action = "Updated"
    else:
        url = f"https://api.github.com/orgs/{ORG_NAME}/rulesets"
        ruleset = {
            "name": ruleset_name,
            "target": "branch",
            "enforcement": "active",
            "conditions": {
                "ref_name": {
                    "include": ["refs/heads/main", "refs/heads/master"],
                    "exclude": []
                },
                "repository_name": {
                    "include": repos,
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
                        "required_approving_review_count": 1
                    }
                },
                {
                    "type": "required_pull_request",
                    "parameters": {
                        "required": True
                    }
                }
            ]
        }
        method = requests.post
        action = "Created"
    
    print(f"Sending request to {action.lower()} ruleset with the following data:")
    print(json.dumps(ruleset, indent=2))
    
    response = method(url, headers=headers, data=json.dumps(ruleset))
    
    print(f"Response status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Response content: {response.text}")
    
    if response.status_code in [200, 201]:
        ruleset = response.json()
        print(f"Successfully {action.lower()} organization ruleset '{ruleset['name']}'")
        return ruleset['id']
    else:
        print(f"Failed to {action.lower()} organization ruleset: {response.status_code} - {response.text}")
        error_data = response.json()
        if 'errors' in error_data and isinstance(error_data['errors'], list):
            for error in error_data['errors']:
                if isinstance(error, dict):
                    print(f"Error: {error.get('message', 'Unknown error')}")
                    print(f"Location: {error.get('resource', 'Unknown')} - {error.get('field', 'Unknown')}")
                else:
                    print(f"Error: {error}")
        elif 'message' in error_data:
            print(f"Error message: {error_data['message']}")
        return None

def main():
    try:
        repos = load_repositories('../production_repos.json')
        print(f"Found {len(repos)} repositories in production-repos.json")
        ruleset_id = create_or_update_org_ruleset(repos)
        if ruleset_id:
            print(f"Ruleset created or updated with ID: {ruleset_id}")
        else:
            print("Failed to create or update ruleset")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
