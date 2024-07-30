import requests
import json
import os

# Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ORGANIZATION = 'hmcts-test'
RULESET_NAME = 'test-ruleset'
REPO_FILE = 'production-repos.json'

# Headers for authentication
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28'
}

def load_repositories(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def create_custom_property(org, property_name, property_data):
    url = f'https://api.github.com/orgs/{org}/properties/schema'
    data = {
        "name": property_name,
        "type": property_data['type'],
        "required": property_data.get('required', False),
        "description": property_data.get('description', '')
    }
    if property_data['type'] == 'single_select':
        data['allowed_values'] = property_data['allowed_values']
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    print(f"Created custom property: {property_name}")
    return response.json()

def set_repo_custom_property(org, repo, properties):
    url = f'https://api.github.com/repos/{org}/{repo}/properties/values'
    data = {"properties": [{"property_name": k, "value": v} for k, v in properties.items()]}
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()
    print(f"Set custom properties for {repo}")
    return response.json()

def get_or_create_ruleset(org, ruleset_name, repos):
    url = f'https://api.github.com/orgs/{org}/rulesets'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    rulesets = response.json()
    
    for ruleset in rulesets:
        if ruleset['name'] == ruleset_name:
            print(f"Updating existing ruleset: {ruleset_name}")
            return update_ruleset(org, ruleset['id'], repos)
    
    print(f"Creating new ruleset: {ruleset_name}")
    return create_ruleset(org, ruleset_name, repos)

def update_ruleset(org, ruleset_id, repos):
    url = f'https://api.github.com/orgs/{org}/rulesets/{ruleset_id}'
    data = {
        "conditions": {
            "repository_name": {
                "include": repos,
                "exclude": []
            },
            "ref_name": {
                "include": ["refs/heads/main", "refs/heads/master"],
                "exclude": []
            }
        },
        "rules": [
            {"type": "deletion"},
            {"type": "non_fast_forward"},
            {
                "type": "pull_request",
                "parameters": {
                    "required_approving_review_count": 2,
                    "dismiss_stale_reviews_on_push": False,
                    "require_code_owner_review": False,
                    "require_last_push_approval": True,
                    "required_review_thread_resolution": True
                }
            },
            {"type": "required_linear_history"},
            {
                "type": "required_status_checks",
                "parameters": {
                    "strict_required_status_checks_policy": True,
                    "required_status_checks": [
                        {"context": "ci/lint"},
                        {"context": "ci/test"}
                    ]
                }
            }
        ],
        "enforcement": "active"
    }
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def create_ruleset(org, ruleset_name, repos):
    url = f'https://api.github.com/orgs/{org}/rulesets'
    data = {
        "name": ruleset_name,
        "target": "branch",
        "enforcement": "active",
        "conditions": {
            "repository_name": {
                "include": repos,
                "exclude": []
            },
            "ref_name": {
                "include": ["refs/heads/main", "refs/heads/master"],
                "exclude": []
            }
        },
        "rules": [
            {"type": "deletion"},
            {"type": "non_fast_forward"},
            {
                "type": "pull_request",
                "parameters": {
                    "required_approving_review_count": 2,
                    "dismiss_stale_reviews_on_push": False,
                    "require_code_owner_review": False,
                    "require_last_push_approval": True,
                    "required_review_thread_resolution": True
                }
            },
            {"type": "required_linear_history"},
            {
                "type": "required_status_checks",
                "parameters": {
                    "strict_required_status_checks_policy": True,
                    "required_status_checks": [
                        {"context": "ci/lint"},
                        {"context": "ci/test"}
                    ]
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def main():
    repos = load_repositories(REPO_FILE)
    
    # Define custom properties
    custom_properties = {
        "team": {
            "type": "string",
            "required": True,
            "description": "The team responsible for this repository"
        },
        "criticality": {
            "type": "single_select",
            "required": True,
            "description": "The criticality level of the repository",
            "allowed_values": ["low", "medium", "high"]
        }
    }

    # Create custom properties
    for prop_name, prop_data in custom_properties.items():
        create_custom_property(ORGANIZATION, prop_name, prop_data)

    # Set custom properties for each repository
    for repo in repos:
        properties = {
            "team": "default-team",
            "criticality": "low"
        }
        set_repo_custom_property(ORGANIZATION, repo, properties)

    # Create or update ruleset
    ruleset = get_or_create_ruleset(ORGANIZATION, RULESET_NAME, repos)
    print(json.dumps(ruleset, indent=2))

if __name__ == "__main__":
    main()