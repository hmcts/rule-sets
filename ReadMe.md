# GitHub Repository Rules

This repository contains Terraform code to manage GitHub repository branch protection rules for HMCTS repositories.

## Overview

This Terraform configuration automates the process of setting up branch protection rules across multiple GitHub repositories. It implements a batching system to handle a large number of repositories efficiently while respecting GitHub API rate limits.

## Getting Started

### Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) (version 0.12 or later)
- GitHub Personal Access Token with appropriate permissions

### Configuration

1. Clone this repository:
git clone https://github.com/hmcts/github-repository-rules.git
cd github-repository-rules
Copy
2. Create a `terraform.tfvars` file with your GitHub token:
github_token = "your-github-token-here"
Copy
3. Update the `prod-repos.json` file with the list of repositories you want to manage.

### Usage

1. Initialize Terraform:
terraform init
Copy
2. Plan the changes:
terraform plan -parallelism=1
Copy
3. Apply the changes:
terraform apply -parallelism=1
Copy
## What This Does

- Reads a list of repositories from `prod-repos.json`
- Checks for the existence of 'main' and 'master' branches in each repository
- Applies branch protection rules to existing branches
- Processes repositories in batches to manage API rate limits

## Maintenance

To add or remove repositories, update the `prod-repos.json` file and re-run the Terraform apply command.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/hmcts/github-repository-rules/tags).

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Recent Changes

We recently addressed issues with scaling to a larger number of repositories. Here's a summary of the changes:

1. Implemented a batching system that splits repositories into smaller groups of 20.
2. Processes each batch sequentially with built-in delays between batches.
3. Uses null_resources to manage the batch processing and ensure proper timing.
4. Only applies branch protection rules after all batches have been processed.

These changes allow us to handle a significantly larger number of repositories without overwhelming the GitHub API or causing Terraform to crash. The system is now more scalable for future growth.

## Project Structure

- `main.tf`: Contains the main Terraform configuration for branch protection rules.
- `data.tf`: Defines data sources for GitHub repositories and branches.
- `locals.tf`: Contains local variables for processing repository data.
- `null_resources.tf`: Implements the batching system with delays.
- `outputs.tf`: Defines outputs for branch summaries and counts.
- `prod-repos.json`: List of repositories to manage.

## Troubleshooting

If you encounter API rate limit issues, try increasing the delay between batches in the `null_resources.tf` file.

For any other issues, please open an issue in the GitHub repository.