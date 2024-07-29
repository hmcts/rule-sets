import requests
import os
import sys
import json
from datetime import datetime

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
    "Accept": "application/vnd.github.v3+json"
}

def get_repositories():
    """Read repositories from production-repos.json file."""
    try:
        with open('production-repos.json', 'r') as f:
            repos = json.load(f)
        return repos
    except FileNotFoundError:
        print("Error: production-repos.json file not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in production-repos.json")
        sys.exit(1)

def create_org_ruleset(repos):
    """Create an organization-level ruleset and assign repositories to it using REST API."""
    url = f"https://api.github.com/orgs/{ORG_NAME}/rulesets"
    
    ruleset_name = f"Organization Ruleset - {datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    ruleset_data = {
        "name": ruleset_name,
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [
            {
                "actor_id": 1,
                "actor_type": "OrganizationAdmin",
                "bypass_mode": "always"
            }
        ],
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
            }
        ]
    }
    
    print(f"Sending request to create ruleset with the following data:")
    print(json.dumps(ruleset_data, indent=2))
    
    response = requests.post(url, headers=headers, json=ruleset_data)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Response content: {response.text}")
    
    if response.status_code == 201:
        ruleset = response.json()
        print(f"Successfully created organization ruleset '{ruleset['name']}'")
        return ruleset['id']
    else:
        print(f"Failed to create organization ruleset: {response.status_code} - {response.text}")
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
        repos = get_repositories()
        print(f"Found {len(repos)} repositories in production-repos.json")
        ruleset_id = create_org_ruleset(repos)
        if ruleset_id:
            print(f"Ruleset created with ID: {ruleset_id}")
        else:
            print("Failed to create ruleset")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()