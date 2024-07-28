import requests
import os
import sys

# GitHub organization name
ORG_NAME = "hmcts-test"

# GitHub Personal Access Token
GITHUB_TOKEN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    print("Error: GitHub token not provided")
    sys.exit(1)

# Headers for GitHub API requests
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_repositories():
    """Fetch all repositories in the organization."""
    url = f"https://api.github.com/orgs/{ORG_NAME}/repos?per_page=100"
    repos = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repos.extend(response.json())
        url = response.links.get("next", {}).get("url")
    return [repo["name"] for repo in repos]

def set_branch_protection(repo):
    """Set branch protection rules for a repository."""
    branches_to_try = ["main", "master"]
    
    for branch in branches_to_try:
        url = f"https://api.github.com/repos/{ORG_NAME}/{repo}/branches/{branch}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            protection_url = f"{url}/protection"
            protection_rules = {
                "required_status_checks": {
                    "strict": True,
                    "contexts": ["ci/circleci: build", "security/snyk"]
                },
                "enforce_admins": True,
                "required_pull_request_reviews": {
                    "dismiss_stale_reviews": True,
                    "require_code_owner_reviews": True,
                    "required_approving_review_count": 2
                },
                "restrictions": None
            }
            
            response = requests.put(protection_url, headers=headers, json=protection_rules)
            if response.status_code == 200:
                print(f"Successfully set branch protection for {repo} on branch {branch}")
                return
            else:
                print(f"Failed to set branch protection for {repo} on branch {branch}: {response.status_code} - {response.text}")
                return
    
    print(f"No suitable branch found for {repo}")

def main():
    try:
        repos = get_repositories()
        print(f"Found {len(repos)} repositories")
        for repo in repos:
            set_branch_protection(repo)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()