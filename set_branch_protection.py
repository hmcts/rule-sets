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

def check_existing_ruleset():
    """Check if a ruleset with the same name already exists."""
    url = f"https://api.github.com/orgs/{ORG_NAME}/rulesets"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        rulesets = response.json()
        for ruleset in rulesets:
            if ruleset['name'] == "Default Organization Ruleset":
                return ruleset['id']
    return None

def create_org_ruleset(repos):
    """Create an organization-level ruleset and assign repositories to it using REST API."""
    url = f"https://api.github.com/orgs/{ORG_NAME}/rulesets"
    
    ruleset_data = {
        "name": "Default Organization Ruleset",
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
                "type": "deletion",
                "parameters": {
                    "allow_deletions": False
                }
            },
            {
                "type": "pull_request",
                "parameters": {
                    "dismiss_stale_reviews_on_push": True,
                    "require_code_owner_reviews": False,
                    "required_approving_review_count": 1,
                    "required_review_thread_resolution": True
                }
            }
        ]
    }
    
    print("Sending request with the following data:")
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
        return None

def main():
    try:
        repos = get_repositories()
        print(f"Found {len(repos)} repositories in production-repos.json")
        
        existing_ruleset_id = check_existing_ruleset()
        if existing_ruleset_id:
            print(f"A ruleset with the name 'Default Organization Ruleset' already exists with ID: {existing_ruleset_id}")
            print("Please delete or rename the existing ruleset before creating a new one.")
            sys.exit(1)
        
        ruleset_id = create_org_ruleset(repos)
        if ruleset_id:
            print(f"Ruleset created with ID: {ruleset_id}")
        else:
            print("Failed to create ruleset")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()