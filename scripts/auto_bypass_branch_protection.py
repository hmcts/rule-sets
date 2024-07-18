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

# def bypass_branch_protection(repo, rulesets, admins):
#     for ruleset in rulesets:
#         if ruleset.get('target') == 'branch':
#             print(f"Attempting to update ruleset {ruleset['name']} (ID: {ruleset['id']}) for {repo}")

#             # Prepare bypass actors with valid actor type and ID
#             bypass_actors = [
#                 {
#                     'actor_id': 1,  # ID for OrganizationAdmin
#                     'actor_type': 'OrganizationAdmin',
#                     'bypass_mode': 'always'
#                 }
#             ]

#             # Prepare the full ruleset update payload
#             update_data = {
#                 'name': ruleset['name'],
#                 'target': ruleset['target'],
#                 'enforcement': ruleset['enforcement'],
#                 'bypass_actors': bypass_actors
#             }

#             # Add conditions if present
#             if 'conditions' in ruleset:
#                 update_data['conditions'] = ruleset['conditions']

#             # Add rules if present
#             if 'rules' in ruleset:
#                 update_data['rules'] = ruleset['rules']

#             # Update the ruleset
#             response = requests.put(
#                 f'{API_BASE_URL}/repos/{ORGANIZATION}/{repo}/rulesets/{ruleset["id"]}',
#                 headers=headers,
#                 json=update_data
#             )

#             if response.status_code == 200:
#                 print(f"Successfully updated bypass permissions for ruleset {ruleset['name']} in {repo}")
#             else:
#                 print(f"Error: Failed to update ruleset {ruleset['name']} for {repo}. Status code: {response.status_code}")
#                 print(f"Response: {response.text}")
                
#             # Check the updated ruleset
#             check_response = requests.get(
#                 f'{API_BASE_URL}/repos/{ORGANIZATION}/{repo}/rulesets/{ruleset["id"]}',
#                 headers=headers
#             )
#             print(f"Ruleset check response: {check_response.status_code} - {check_response.text}")

#         time.sleep(1)  # Add a small delay to avoid hitting rate limits

# def main():
#     admins = get_org_admins()
#     print(f"Found {len(admins)} admins in the {ORGANIZATION} organization.")
    
#     repos_with_rulesets = get_repos_with_rulesets()
#     print(f"Found {len(repos_with_rulesets)} repositories with rulesets.")
    
#     for repo, rulesets in repos_with_rulesets:
#         bypass_branch_protection(repo, rulesets, admins)

# if __name__ == "__main__":
#     main()
