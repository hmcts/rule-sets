# GitHub Repository Rules

This repository contains code to manage GitHub repository branch protection rules for HMCTS.

# Overview

This Terraform configuration automates the process of setting up rule sets across multiple GitHub repositories. It implements a batching system to handle a large number of repositories efficiently while respecting GitHub API rate limits.

- [Rate Limits Page](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28)

<!--START_PRODUCTION_COUNT-->
<!--END_PRODUCTION_COUNT-->


## Getting Started

### Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) (version 1.5.7 or later)
- Oauth or PAT Token with appropriate permissions.

### Configuration

1. Clone this repository:

   ```bash
   git clone https://github.com/hmcts/github-repository-rules.git
2. Create a `terraform.tfvars` file with your Oauth token:
3. The python file runs gets ran as a cron job via a GitHub Actions pipeline at midnight and updates the JSON file with new repositories.

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

## Recent Changes

We recently addressed issues with scaling to a larger number of repositories. Here's a summary of the changes:

1. Implemented a batching system that splits repositories into smaller groups of 20.
2. Processes each batch sequentially with built-in delays between batches.
3. Only applies rule sets after all batches have been processed.

These changes allow us to handle a significantly larger number of repositories without overwhelming the GitHub API or causing Terraform to crash. The system is now more scalable for future growth.

## Project Structure

- `main.tf`: Contains the main Terraform configuration for branch protection rules.
- `data.tf`: Defines data sources for GitHub repositories and branches.
- `locals.tf`: Contains local variables for processing repository data.
- `outputs.tf`: Defines outputs for branch summaries and counts.
- `provider.tf`: Terraform/GitHub providers.
- `production-repos.json`: List of repositories to manage.
- `update_raedme.py`: Updates the read me file with stats of the number of prod, dev repositories etc.
- `update-repo-list.py`: Updates the JSON file that contains the number of production/dev repositories.
- `set_org_custom_properties.py`: Creates the custom properties listed in the JSON file on the repositories.
- `pr.yaml`: Pipeline triggers a terraform plan when a PR is raised from master.
- `pipeline.yaml`: Pipeline runs after the PR workflow has succesfully ran and applies the terraform.
- `update-readme.yaml`: This pipeline runs as a cron job every midnight and updates the read me file with new stats.
- `update-repos.json`: This pipeline runs as a cron job and will update the JSON file with new repositories.


## Troubleshooting

- Check your Terraform version and ensure there are no underlying bugs with the provider versions.
- Ensure you have formatted your repository name correctly as it may not pick it up properly.
