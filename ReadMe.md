# GitHub Repository Rules

This repository contains code to manage GitHub repository branch protection rules for HMCTS.

# Overview

This Terraform configuration automates the process of setting up rule sets across multiple GitHub repositories. It implements a batching system to handle a large number of repositories efficiently while respecting GitHub API rate limits.

- [Rate Limits Page](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28)

<!--START_PRODUCTION_COUNT-->

| **Repository Type**       | **Count** |
|---------------------------|-----------|
| Production Repositories   | [11](https://github.com/hmcts/github-repository-rules/blob/DTSPO-18104-typo-file-V2/production-repos.json)        |
| Development Repositories  | 0        |
<!--END_PRODUCTION_COUNT-->

## Getting Started

### Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) (version 1.5.7 or later)
- Oauth or PAT Token with appropriate permissions.


## What This Does

- Reads a list of repositories from `production-repos.json`
- Creates rule sets on the repositories read from the JSON file, applying standardisation across all repositories.
- Creates custom properties to tag and categorize repositories, such as marking repositories as "in production."
- Processes repositories in batches to manage API rate limits.


## Maintenance

To add or remove repositories follow the below:

1. Open a fresh PR from the master branch ensuring you have pulled down recent changes to the master branch.
2. Applies standardized rule sets to repositories listed in the `production-repos.json` file, ensuring consistent management and configuration across all repositories.
3. Create a PR and allow the GH Actions pipeline to run a Terraform Plan to confirm changes are accepted.
4. Once this first pipeline checks out, the second pipeline will apply your changes and update the branch protection rules.
5. Once applied delete your branch.


## Troubleshooting

- Check your Terraform version and ensure there are no underlying bugs with the provider versions.
- Ensure you have formatted your repository name correctly as it may not pick it up properly.
