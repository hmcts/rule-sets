import requests
import os
import sys
import json

# GitHub organization name
ORG_NAME = "hmcts-test"

# GitHub PAT Token (Personal Access Token)
GITHUB_TOKEN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("PAT_TOKEN")

# Check if the PAT token is available, else exit
if not GITHUB_TOKEN:
    print("Error: PAT_TOKEN not found in environment variables or command line arguments")
    sys.exit(1)

# Masked token print for debugging purposes
print(f"Using token: {GITHUB_TOKEN[:4]}...{GITHUB_TOKEN[-4:]}")

# Headers for GitHub API requests
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_repositories():
    """
    Reads repositories from the production-repos.json file.
    
    Returns:
        list: List of repository names.
    """
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

def apply_branch_protection(org, repo, branch):
    """
    Applies branch protection rules to a specified branch of a repository.
    
    Args:
        org (str): Organization name.
        repo (str): Repository name.
        branch (str): Branch name.
    """
    # URL for branch protection API
    url = f"https://api.github.com/repos/{org}/{repo}/branches/{branch}/protection"
    
    # Branch protection rules
    protection_data = {
        "required_status_checks": {
            "strict": True,
            "contexts": []
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": True,
            "required_approving_review_count": 1
        },
        "restrictions": None,
        "required_linear_history": True
    }
    
    # Sending the PUT request to apply branch protection
    response = requests.put(url, headers=headers, json=protection_data)
    
    # Logging the response
    print(f"Applying branch protection to {repo}/{branch}")
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    
    # Checking the response status
    if response.status_code in [200, 201]:
        print(f"Successfully applied branch protection to {repo}/{branch}")
    else:
        print(f"Failed to apply branch protection to {repo}/{branch}: {response.status_code} - {response.text}")

def main():
    """
    Main function to apply branch protection rules to all repositories listed in production-repos.json.
    """
    try:
        # Get the list of repositories
        repos = get_repositories()
        print(f"Found {len(repos)} repositories in production-repos.json")
        
        # Apply branch protection to both 'main' and 'master' branches for each repository
        for repo in repos:
            apply_branch_protection(ORG_NAME, repo, "main")
            apply_branch_protection(ORG_NAME, repo, "master")
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
