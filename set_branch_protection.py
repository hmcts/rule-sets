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
    print(f"Response content: {response.text}")
    
    if response.status_code == 201:
        ruleset = response.json()
        print(f"Successfully created organization ruleset '{ruleset['name']}'")
        return ruleset['id']
    else:
        print(f"Failed to create organization ruleset: {response.status_code} - {response.text}")
        return None

def set_branch_protection(repo, branch):
    """Set branch protection rules for a specific repository and branch."""
    url = f"https://api.github.com/repos/{ORG_NAME}/{repo}/branches/{branch}/protection"
    
    protection_data = {
        "required_linear_history": True,
        "allow_force_pushes": False,
        "allow_deletions": False
    }
    
    response = requests.put(url, headers=headers, json=protection_data)
    
    if response.status_code in [200, 201]:
        print(f"Successfully set branch protection for {repo}/{branch}")
    else:
        print(f"Failed to set branch protection for {repo}/{branch}: {response.status_code} - {response.text}")

def main():
    try:
        repos = get_repositories()
        print(f"Found {len(repos)} repositories in production-repos.json")
        
        ruleset_id = create_org_ruleset(repos)
        if ruleset_id:
            print(f"Ruleset created with ID: {ruleset_id}")
        else:
            print("Failed to create ruleset")
        
        for repo in repos:
            for branch in ['main', 'master']:
                set_branch_protection(repo, branch)
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()