import requests
import yaml
import json
import os
from urllib.parse import urlparse, parse_qs

# URLs to the remote YAML and JSON files
urls = [
    'https://raw.githubusercontent.com/hmcts/sds-jenkins-config/master/environment-approvals.yml',
    'https://raw.githubusercontent.com/hmcts/cnp-jenkins-config/master/environment-approvals.yml',
    'https://raw.githubusercontent.com/hmcts/cnp-jenkins-config/master/terraform-infra-approvals/global.json',
    'https://raw.githubusercontent.com/hmcts/sds-jenkins-config/master/terraform-infra-approvals/global.json',
]

# Function to fetch and parse the files
def fetch_and_parse(url):
    response = requests.get(url)
    if url.endswith('.yml') or url.endswith('.yaml'):
        return yaml.safe_load(response.text)
    elif url.endswith('.json'):
        return json.loads(response.text)
    return None

# Function to clean the repository name
def clean_repo_name(repo_url):
    parsed_url = urlparse(repo_url)
    # Extract the path part of the URL and remove leading '/'
    path = parsed_url.path.lstrip('/')
    # Remove the .git suffix if present
    repo_name = path.replace('.git', '')
    # Split the path to get the repository name
    repo_name = repo_name.split('/')[-1]
    return repo_name

# Collect all repositories from the parsed files
all_repos = []

for url in urls:
    data = fetch_and_parse(url)
    if url.endswith('.yml') or url.endswith('.yaml'):
        # For YAML files
        for key in data:
            if isinstance(data[key], list):
                for item in data[key]:
                    if 'repo' in item:
                        repo_name = clean_repo_name(item['repo'])
                        all_repos.append(repo_name)
    elif url.endswith('.json'):
        # For JSON files
        if 'module_calls' in data:
            for item in data['module_calls']:
                if 'source' in item:
                    repo_name = clean_repo_name(item['source'])
                    all_repos.append(repo_name)

# Remove duplicates and ensure no erroneous "https" entries
all_repos = list(set(all_repos))
all_repos = [repo for repo in all_repos if repo != "https"]

# Determine the path for the output file
repo_file = os.path.join(os.path.dirname(__file__), '../production-repos.json')

# Update the local file
with open(repo_file, 'w') as f:
    json.dump(all_repos, f, indent=2)
