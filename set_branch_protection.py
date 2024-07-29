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

print(f"Using token: {GITHUB_TOKEN[:4]}...{GITHUB_TOKEN[-4:]}")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_repositories():
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
    url = f"https://api.github.com/orgs/{ORG_NAME}/rulesets"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        rulesets = response.json()
        for ruleset in rulesets:
            if ruleset['name'] == "Organization-wide Branch Protection Rules":
                return ruleset['id']
    return None

def create_org_ruleset(repos):
    url = f"https://api.github.com/orgs/{ORG_NAME}/rulesets"
    
    ruleset_data = {
        "name": "Organization-wide Branch Protection Rules",
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
                    "required_approving_review_count": 2,
                    "dismiss_stale_reviews": True,
                    "require_code_owner_reviews": True
                }
            }
        ]
    }
    
    print("Creating organization ruleset with the following data:")
    print(json.dumps(ruleset_data, indent=2))
    
    response = requests.post(url, headers=headers, json=ruleset_data)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    
    if response.status_code in [201, 200]:
        print("Successfully created organization ruleset")
        return response.json().get('id')
    else:
        print(f"Failed to create organization ruleset: {response.status_code} - {response.text}")
        return None

def update_org_ruleset(ruleset_id, repos):
    url = f"https://api.github.com/orgs/{ORG_NAME}/rulesets/{ruleset_id}"
    
    ruleset_data = {
        "name": "Organization-wide Branch Protection Rules",
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
        }
    }
    
    print("Updating organization ruleset with the following data:")
    print(json.dumps(ruleset_data, indent=2))
    
    response = requests.put(url, headers=headers, json=ruleset_data)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    
    if response.status_code in [200, 204]:
        print("Successfully updated organization ruleset")
    else:
        print(f"Failed to update organization ruleset: {response.status_code} - {response.text}")

def main():
    try:
        repos = get_repositories()
        print(f"Found {len(repos)} repositories in production-repos.json")
        
        ruleset_id = get_existing_ruleset()
        if ruleset_id:
            print("Existing ruleset found. Updating...")
            update_org_ruleset(ruleset_id, repos)
        else:
            print("No existing ruleset found. Creating new one...")
            create_org_ruleset(repos)
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
