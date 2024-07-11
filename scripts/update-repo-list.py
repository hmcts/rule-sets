import requests
import yaml
import json
import re
import os

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
                        repo_name = item['repo'].split('/')[-1].replace('.git', '').split(':')[0]
                        all_repos.append(repo_name)
    elif url.endswith('.json'):
        # For JSON files
        if 'module_calls' in data:
            for item in data['module_calls']:
                if 'source' in item:
                    # Extract the repository name from the 'source' value and remove the .git and any branch/ref suffix
                    match = re.search(r'git@github.com:(.*?)(\.git|$)', item['source'])
                    if match:
                        repo_name = match.group(1).split('/')[-1].replace('.git', '').split(':')[0]
                        all_repos.append(repo_name)

# Remove duplicates
all_repos = list(set(all_repos))

# Determine the path for the output file
repo_file = os.path.join(os.path.dirname(__file__), '../production-repos.json')

# Update the local file
with open(repo_file, 'w') as f:
    json.dump(all_repos, f, indent=2)
