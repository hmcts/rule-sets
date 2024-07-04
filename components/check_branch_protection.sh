#!/bin/bash

# Read the repositories from the JSON file
repositories=$(jq -r '.[]' test-repos.json)

# Define the branches you want to check
branches=("master" "main") # Add more branches if needed

# Loop over each repo and branch
for repo in $repositories; do
  for branch in "${branches[@]}"; do
    # Check if the branch protection rule exists
    if gh api repos/$repo/branches/$branch/protection; then
      echo "Branch protection rule exists for $repo:$branch"
    else
      echo "Branch protection rule does not exist for $repo:$branch"
      # Run your Terraform code here to create the branch protection rule
      terraform apply -var="repo=$repo" -var="branch=$branch"
    fi
  done
done
