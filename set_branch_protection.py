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
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        if isinstance(data, list) and all(isinstance(item, str) for item in data):
            return data
        else:
            raise ValueError("JSON data should be a list of repository names")
    except Exception as e:
        print(f"Error loading repositories from {file_path}: {e}")
        raise

def get_ruleset_by_name(org, ruleset_name):
    url = f'https://api.github.com/orgs/{org}/rulesets'
    print(f"Fetching rulesets from URL: {url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        rulesets = response.json()
        for ruleset in rulesets:
            if ruleset['name'] == ruleset_name:
                return ruleset
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching rulesets: {e}")
        raise

def update_ruleset(org, ruleset_id, data):
    url = f'https://api.github.com/orgs/{org}/rulesets/{ruleset_id}'
    print(f"Updating ruleset at URL: {url}")
    print(f"Request Headers: {headers}")
    print(f"Request Data: {json.dumps(data, indent=4)}")
    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error updating ruleset: {e}")
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        raise

def create_ruleset(org, data):
    url = f'https://api.github.com/orgs/{org}/rulesets'
    print(f"Creating ruleset at URL: {url}")
    print(f"Request Headers: {headers}")
    print(f"Request Data: {json.dumps(data, indent=4)}")
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating ruleset: {e}")
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        raise

def set_repo_custom_property(org, repo, properties):
    url = f'https://api.github.com/repos/{org}/{repo}/properties/values'
    data = {
        "properties": [{"property_name": k, "value": v} for k, v in properties.items()]
    }
    try:
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error setting custom properties for {repo}: {e}")
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        raise

try:
    # Load repositories from JSON file
    target_repositories = load_repositories(REPO_FILE)

    # Define custom properties
    custom_properties = {
        "team": "default-team",
        "criticality": "low"
    }

    # Set custom properties for each repository
    for repo in target_repositories:
        set_repo_custom_property(ORGANIZATION, repo, custom_properties)
        print(f"Set custom properties for {repo}")

    # Check if a ruleset with the same name already exists
    matching_ruleset = get_ruleset_by_name(ORGANIZATION, RULESET_NAME)

    bypass_actors = [
        {
            "actor_id": 4067333,
            "actor_type": "Team",
            "bypass_mode": "always"
        }
    ]

    ref_name_conditions = {
        "exclude": [],
        "include": [
            "~DEFAULT_BRANCH",
            "refs/heads/master",
            "refs/heads/main"
        ]
    }

    def ensure_branches_in_conditions(conditions, ref_name_conditions):
        if 'ref_name' not in conditions:
            conditions['ref_name'] = ref_name_conditions
        else:
            current_includes = set(conditions['ref_name'].get('include', []))
            current_includes.update(ref_name_conditions['include'])
            conditions['ref_name']['include'] = list(current_includes)
            current_excludes = set(conditions['ref_name'].get('exclude', []))
            current_excludes.update(ref_name_conditions['exclude'])
            conditions['ref_name']['exclude'] = list(current_excludes)

    if matching_ruleset:
        # Ruleset with the same name exists, update it
        ruleset_id = matching_ruleset['id']

        # Ensure conditions exist in the ruleset
        if 'conditions' not in matching_ruleset:
            matching_ruleset['conditions'] = {}

        # Check and update the repository_name condition
        if 'repository_name' in matching_ruleset['conditions']:
            matching_ruleset['conditions']['repository_name']['include'] = target_repositories
            matching_ruleset['conditions']['repository_name']['protected'] = True
        else:
            print("'repository_name' not found in ruleset conditions, adding it.")
            matching_ruleset['conditions']['repository_name'] = {
                'include': target_repositories,
                'exclude': [],
                'protected': True
            }

        # Ensure the ref_name conditions include the necessary branches
        ensure_branches_in_conditions(matching_ruleset['conditions'], ref_name_conditions)

        # Enable enforcement
        matching_ruleset['enforcement'] = 'active'

        # Add or update bypass_actors
        matching_ruleset['bypass_actors'] = bypass_actors

        # Update the ruleset on GitHub
        updated_ruleset = update_ruleset(ORGANIZATION, ruleset_id, matching_ruleset)

        print("Updated Ruleset:")
        print(json.dumps(updated_ruleset, indent=4))
    else:
        # No matching ruleset, create a new one
        new_ruleset_data = {
            "name": RULESET_NAME,
            "target": "branch",
            "enforcement": "active",
            "conditions": {
                "ref_name": ref_name_conditions,
                "repository_name": {
                    "include": target_repositories,
                    "exclude": [],
                    "protected": True
                }
            },
            "rules": [
                {
                    "type": "deletion"
                },
                {
                    "type": "non_fast_forward"
                },
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
                {
                    "type": "required_linear_history"
                },
                {
                    "type": "required_status_checks",
                    "parameters": {
                        "strict_required_status_checks_policy": True,
                        "do_not_enforce_on_create": False,
                        "required_status_checks": [
                            {
                                "context": "ci/lint"
                            },
                            {
                                "context": "ci/test"
                            }
                        ]
                    }
                }
            ],
            "bypass_actors": bypass_actors
        }
        created_ruleset = create_ruleset(ORGANIZATION, new_ruleset_data)
        print("Created New Ruleset:")
        print(json.dumps(created_ruleset, indent=4))

except Exception as e:
    print(f"An error occurred: {e}")
