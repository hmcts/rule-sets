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

def get_existing_ruleset(name):
    url = f"https://api.github.com/orgs/{ORG_NAME}/rulesets"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        rulesets = response.json()
        for ruleset in rulesets:
            if ruleset['name'] == name:
                return ruleset['id']
    return None

def create_or_update_org_ruleset(repos):
    """Create or update an organization-level ruleset and assign repositories to it using REST API."""
    ruleset_name = "Default Organization Ruleset"
    existing_ruleset_id = get_existing_ruleset(ruleset_name)
    
    url = f"https://api.github.com/orgs/{ORG_NAME}/rulesets"
    method = requests.post
    action = "Created"

    if existing_ruleset_id:
        url = f"{url}/{existing_ruleset_id}"
        method = requests.put
        action = "Updated"
    
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
                "type": "required_linear_history",
                "parameters": {}
            },
            {
                "type": "required_pull_request_reviews",
                "parameters": {
                    "required_approving_review_count": 1,
                    "require_code_owner_review": False,
                    "dismiss_stale_reviews_on_push": True
                }
            },
            {
                "type": "required_status_checks",
                "parameters": {
                    "strict": True,
                    "contexts": []
                }
            },
            {
                "type": "required_signatures",
                "parameters": {}
            }
        ]
    }
    
    print(f"Sending request to {action.lower()} ruleset with the following data:")
    print(json.dumps(ruleset_data, indent=2))
    
    response = method(url, headers=headers, json=ruleset_data)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Response content: {response.text}")
    
    if response.status_code in [200, 201]:
        ruleset = response.json()
        print(f"Successfully {action.lower()} organization ruleset '{ruleset['name']}'")
        re
