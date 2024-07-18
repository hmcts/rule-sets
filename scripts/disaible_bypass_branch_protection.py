# import requests
# import json
# import sys
# import os
# import time

# # GitHub configuration
# GITHUB_TOKEN = os.environ.get('GITHUB_OAUTH_TOKEN')
# ORGANIZATION = 'hmcts-test'
# API_BASE_URL = 'https://api.github.com'

# headers = {
#     'Authorization': f'token {GITHUB_TOKEN}',
#     'Accept': 'application/vnd.github+json'
# }

# def get_org_admins():
#     admins = []
#     page = 1
#     while True:
#         response = requests.get(
#             f'{API_BASE_URL}/orgs/{ORGANIZATION}/members',
#             headers=headers,
#             params={'role': 'admin', 'page': page, 'per_page': 100}
#         )
#         if response.status_code == 200:
#             page_admins = response.json()
#             if not page_admins:
#                 break
#             admins.extend(page_admins)
#             page += 1
#         else:
#             print(f"Error: Failed to fetch organization admins. Status code: {response.status_code}")
#             sys.exit(1)
#     return admins

# def get_repos_with_rulesets():
#     repos_with_rulesets = []
#     page = 1
#     while True:
#         response = requests.get(
#             f'{API_BASE_URL}/orgs/{ORGANIZATION}/repos',
#             headers=headers,
#             params={'page': page, 'per_page': 100}
#         )
#         if response.status_code == 200:
#             page_repos = response.json()
#             if not page_repos:
#                 break
#             for repo in page_repos:
#                 rulesets = get_repo_rulesets(repo['name'])
#                 if rulesets:
#                     repos_with_rulesets.append((repo['name'], rulesets))
#             page += 1
#         else:
#             print(f"Error: Failed to fetch repositories. Status code: {response.status_code}")
#             sys.exit(1)
#     return repos_with_rulesets

# def get_repo_rulesets(repo):
#     response = requests.get(
#         f'{API_BASE_URL}/repos/{ORGANIZATION}/{repo}/rulesets',
#         headers=headers
#     )
#     if response.status_code == 200:
#         return response.json()
#     print(f"Error fetching rulesets for {repo}. Status code: {response.status_code}")
#     return []

# def disable_bypass_actors(repo, ruleset):
#     # Remove bypass actors
#     update_data = {
#         'name': ruleset['name'],
#         'target': ruleset['target'],
#         'enforcement': ruleset['enforcement'],
#         'bypass_actors': []
#     }

#     # Add conditions if present
#     if 'conditions' in ruleset:
#         update_data['conditions'] = ruleset['conditions']

#     # Add rules if present
#     if 'rules' in ruleset:
#         update_data['rules'] = ruleset['rules']

#     # Update the ruleset
#     response = requests.put(
#         f'{API_BASE_URL}/repos/{ORGANIZATION}/{repo}/rulesets/{ruleset["id"]}',
#         headers=headers,
#         json=update_data
#     )

#     if response.status_code == 200:
#         print(f"Successfully removed bypass actors for ruleset {ruleset['name']} in {repo}")
#     else:
#         print(f"Error: Failed to remove bypass actors for ruleset {ruleset['name']} in {repo}. Status code: {response.status_code}")
#         print(f"Response: {response.text}")

# def main():
#     admins = get_org_admins()
#     print(f"Found {len(admins)} admins in the {ORGANIZATION} organization.")
    
#     repos_with_rulesets = get_repos_with_rulesets()
#     print(f"Found {len(repos_with_rulesets)} repositories with rulesets.")
    
#     for repo, rulesets in repos_with_rulesets:
#         for ruleset in rulesets:
#             if ruleset.get('target') == 'branch':
#                 disable_bypass_actors(repo, ruleset)
#                 time.sleep(1)  # Add a small delay to avoid hitting rate limits

# if __name__ == "__main__":
#     main()
