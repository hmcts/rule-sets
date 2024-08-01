# GitHub Repository Rules

This repository contains code to manage GitHub repository branch protection rules for HMCTS.

## Overview

This Terraform configuration automates the process of setting up branch protection rules across multiple GitHub repositories. It implements a batching system to handle a large number of repositories efficiently while respecting GitHub API rate limits.

- [Rate Limits Page](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28)

<!--START_PRODUCTION_COUNT-->

**Production Repositories Count:** There are currently **9** repositories marked as in production.
<!--END_PRODUCTION_COUNT-->

## Getting Started

### Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) (version 1.5.7 or later)
- GitHub Personal Access Token with appropriate permissions.

### Configuration

1. Clone this repository:
git clone https://github.com/hmcts/github-repository-rules.git
2. Create a `terraform.tfvars` file with your GitHub token:
3. The python file runs as a cron job via GitHub Actions pipeline at midnight and updates the JSON file with new repositories.

## What This Does

- Reads a list of repositories from `prod-repos.json`
- Checks for the existence of 'main' and 'master' branches in each repository.
- Applies branch protection rules to existing branches.
- Processes repositories in batches to manage API rate limits.

## Maintenance

To add or remove repositories follow the below:

1. Open a fresh PR from the master branch ensuring you have pulled down recent changes to the master branch.
2. Update the `prod-repos.json` file with any repository you want. Ensure that its in the format of just the repo name eg: "github-repository-rules"
3. Create a PR and allow the GH Actions pipeline to run a Terraform Plan to confirm changes are accepted.
4. Once this first pipeline checks out, the second pipeline will apply your changes and update the branch protection rules.
5. Once applied delete your branch.

## Recent Changes

We recently addressed issues with scaling to a larger number of repositories. Here's a summary of the changes:

1. Implemented a batching system that splits repositories into smaller groups of 20.
2. Processes each batch sequentially with built-in delays between batches.
3. Only applies branch protection rules after all batches have been processed.

These changes allow us to handle a significantly larger number of repositories without overwhelming the GitHub API or causing Terraform to crash. The system is now more scalable for future growth.

## Project Structure

- `main.tf`: Contains the main Terraform configuration for branch protection rules.
- `data.tf`: Defines data sources for GitHub repositories and branches.
- `locals.tf`: Contains local variables for processing repository data.
- `outputs.tf`: Defines outputs for branch summaries and counts.
- `prod-repos.json`: List of repositories to manage.

## Troubleshooting

- Check your Terraform version and ensure there are no underlying bugs with the provider versions.
- Ensure you have formatted your repository name correctly as it may not pick it up properly.
