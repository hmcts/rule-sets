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

def update_branch_protection(repo, branch):
    """Update branch protection for a specific repository and branch."""
    url = f"https://api.github.com/repos/{ORG_NAME}/{repo}/branches/{branch}/protection"
    
    protection_data = {
        "required_status_checks": None,
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "required_approving_review_count": 1
        },
        "restrictions": None,
        "required_linear_history": True,
        "allow_force_pushes": False,
        "allow_deletions": False
    }
    
    print(f"Updating branch protection for {repo}/{branch}")
    response = requests.put(url, headers=headers, json=protection_data)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    
    if response.status_code in [200, 201]:
        print(f"Successfully updated branch protection for {repo}/{branch}")
    else:
        print(f"Failed to update branch protection for {repo}/{branch}: {response.status_code} - {response.text}")

def main():
    try:
        repos = get_repositories()
        print(f"Found {len(repos)} repositories in production-repos.json")
        
        for repo in repos:
            for branch in ['main', 'master']:
                update_branch_protection(repo, branch)
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()