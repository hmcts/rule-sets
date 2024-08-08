import os
import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# GitHub API base URL
API_BASE = "https://api.github.com"

# Get OAuth token from environment variable
TOKEN = os.environ.get('OAUTH_TOKEN')
if not TOKEN:
    raise ValueError("OAUTH_TOKEN environment variable is not set")

# Your organisation name
ORG_NAME = "hmcts"

# Headers for API requests
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def define_custom_property(org_name):
    """
    Define a custom property for the organisation.

    Args:
        org_name (str): The name of the GitHub organisation.

    Returns:
        int: The status code of the API response.

    Raises:
        requests.RequestException: If the API request fails.
    """
    url = f"{API_BASE}/orgs/{org_name}/properties/schema/is_production"
    data = {
        "value_type": "true_false",
        "required": False,
        "default_value": "",
        "description": "Indicates if the repository is in production",
        "allowed_values": None,  # Set to None as required by API
        "values_editable_by": "org_and_repo_actors"
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code != 200:
        logging.error(f"Failed to define custom property for {org_name}: {response.json().get('message', 'Unknown error')}")
    response.raise_for_status()
    return response.status_code

def set_custom_properties(repo_full_name, properties):
    """
    Set custom properties for a repository.

    Args:
        repo_full_name (str): The full name of the repository (org/repo).
        properties (dict): The custom properties to set.

    Returns:
        int: The status code of the API response.

    Raises:
        requests.RequestException: If the API request fails.
    """
    owner, repo = repo_full_name.split('/')
    url = f"{API_BASE}/repos/{owner}/{repo}/properties/values"
    data = {
        "properties": [
            {"property_name": key, "value": value}
            for key, value in properties.items()
        ]
    }
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code != 204:
        logging.error(f"Failed to set properties for {repo_full_name}: {response.json().get('message', 'Unknown error')}")
    response.raise_for_status()
    return response.status_code

def get_custom_properties(repo_full_name):
    """
    Get custom properties for a repository.

    Args:
        repo_full_name (str): The full name of the repository (org/repo).

    Returns:
        dict: The custom properties of the repository.

    Raises:
        requests.RequestException: If the API request fails.
    """
    owner, repo = repo_full_name.split('/')
    url = f"{API_BASE}/repos/{owner}/{repo}/properties/values"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def load_production_repos():
    """
    Load production repositories from production-repos.json file.

    Returns:
        list: A list of production repositories.
    """
    script_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(script_dir, '../production-repos.json')
    
    try:
        with open(json_file_path, 'r') as f:
            repos = json.load(f)
            if not isinstance(repos, list):
                raise ValueError("JSON content is not a list")
            return repos
    except FileNotFoundError:
        logging.error(f"Error: 'production-repos.json' not found at {os.path.abspath(json_file_path)}")
        logging.error("Current working directory: %s", os.getcwd())
        logging.error("Contents of the current directory: %s", os.listdir('.'))
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {json_file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error reading {json_file_path}: {e}")
        raise

# Define the custom property at the organisation level
try:
    status = define_custom_property(ORG_NAME)
    logging.info(f"Defined custom property for {ORG_NAME}: Status {status}")
except requests.RequestException as e:
    logging.error(f"Failed to define custom property for {ORG_NAME}: {str(e)}")

# Load production repositories
production_repos = load_production_repos()

logging.info(f"Repositories found in production-repos.json:")
for repo in production_repos:
    logging.info(f"- {repo}")

# Apply custom properties to each repository and verify
for repo_name in production_repos:
    repo_full_name = f"{ORG_NAME}/{repo_name}"
    custom_properties = {
        "is_production": "true"
    }

    logging.info(f"\nSetting custom property for: {repo_name}")
    try:
        status = set_custom_properties(repo_full_name, custom_properties)
        logging.info(f"Set properties for {repo_full_name}: Status {status}")

        # Verify the properties were set correctly
        retrieved_properties = get_custom_properties(repo_full_name)
        logging.info(f"Custom properties for {repo_full_name}: {retrieved_properties}")

    except requests.RequestException as e:
        logging.error(f"Failed to set properties for {repo_full_name}: {str(e)}")

logging.info("\nScript execution completed.")
