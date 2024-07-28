#!/bin/bash

# GitHub organization name
ORG_NAME="hmcts-test"

# GitHub Personal Access Token
GITHUB_TOKEN="$1"

# Ruleset configuration
RULESET_NAME="Default Ruleset"
RULESET_TARGET="branch"
RULESET_ENFORCEMENT="active"

# Create the ruleset
response=$(curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/orgs/$ORG_NAME/rulesets \
  -d '{
    "name": "'"$RULESET_NAME"'",
    "target": "'"$RULESET_TARGET"'",
    "enforcement": "'"$RULESET_ENFORCEMENT"'",
    "conditions": {
      "ref_name": {
        "include": ["refs/heads/main", "refs/heads/master"],
        "exclude": []
      }
    },
    "rules": {
      "creation": true,
      "update": true,
      "deletion": false,
      "required_linear_history": true,
      "required_signatures": true,
      "pull_request": {
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": true,
        "required_approving_review_count": 2,
        "required_review_thread_resolution": true
      },
      "required_status_checks": {
        "strict": true,
        "contexts": ["ci/circleci: build", "security/snyk"]
      }
    }
  }')

echo "$response"

# Check if the ruleset was created successfully
if [[ $(echo "$response" | jq '.id') != "null" ]]; then
  echo "Ruleset created successfully"
  exit 0
else
  echo "Failed to create ruleset"
  exit 1
fi