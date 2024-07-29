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

def get_existing_ruleset():
    """Check for existing ruleset and return its ID if found."""
    url = f"https://api.github.com/orgs/{ORG_NAME}/rulesets"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        rulesets = response.json()
        for ruleset in rulesets:
            if ruleset['name'].startswith("Org Ruleset - Branch Protection"):
                return ruleset['id']
    return None

def create_or_update_org_ruleset(repos, existing_ruleset_id=None):
    """Create or update an organization-level ruleset for branch protection."""
    if existing_ruleset_id:
        url = f"https://api.github.com/orgs/{ORG_NAME}/rulesets/{existing_ruleset_id}"
        method = requests.patch
    else:
        url = f"https://api.github.com/orgs/{ORG_NAME}/rulesets"
        method = requests.post

    ruleset_name = "Org Ruleset - Branch Protection"
    
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
                "type": "branch_name_pattern",
                "parameters": {
                    "name": "main",
                    "negate": False
                }
            },
            {
                "type": "non_fast_forward",
                "parameters": {}
            }
        ]
    }
    
    print(f"Sending request to {'update' if existing_ruleset_id else 'create'} ruleset with the following data:")
    print(json.dumps(ruleset_data, indent=2))
    
    response = method(url, headers=headers, json=ruleset_data)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    
    if response.status_code in [200, 201]:
        ruleset = response.json()
        print(f"Successfully {'updated' if existing_ruleset_id else 'created'} organization ruleset '{ruleset['name']}'")
        return ruleset['id']
    else:
        print(f"Failed to {'update' if existing_ruleset_id else 'create'} organization ruleset: {response.status_code} - {response.text}")
        return None

def main():
    try:
        repos = get_repositories()
        print(f"Found {len(repos)} repositories in production-repos.json")
        
        existing_ruleset_id = get_existing_ruleset()
        if existing_ruleset_id:
            print(f"Found existing ruleset with ID: {existing_ruleset_id}")
        
        ruleset_id = create_or_update_org_ruleset(repos, existing_ruleset_id)
        if ruleset_id:
            print(f"Ruleset {'updated' if existing_ruleset_id else 'created'} with ID: {ruleset_id}")
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