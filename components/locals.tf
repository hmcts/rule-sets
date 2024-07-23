locals {
  # List of repositories to exclude from the production-repos.json file
  excluded_repositories = ["github-repository-rules"]

  # Read repositories from JSON file
  all_repositories = jsondecode(data.local_file.repos_json.content)

  # Filter out excluded repos
  included_repositories = [
    for repo in local.all_repositories : repo
    if !contains(local.excluded_repositories, repo)
  ]

  branches_to_check = ["main", "master"]
  batch_size        = 10

  # Split repositories into batches of 10 to help handle the API Rate limits
  repo_batches = chunklist(local.included_repositories, local.batch_size)

  repo_branch_combinations = flatten([
    for batch in local.repo_batches : [
      for repo in batch : [
        for branch in local.branches_to_check : {
          repo   = repo
          branch = branch
        }
      ]
    ]
  ])

  # Create a map of existing branches
  existing_branches = {
    for key, branch in data.github_branch.existing_branches :
    key => branch
  }

  # Checks if a main/master branch exists on the repositories
  branch_summary = {
    for repo in local.included_repositories :
    repo => {
      main   = contains(keys(local.existing_branches), "${repo}:main")
      master = contains(keys(local.existing_branches), "${repo}:master")
    }
  }

  env_display_names = {
    sbox    = "Sandbox"
    prod    = "Production"
    nonprod = "Non-Production"
    test    = "Test"
    staging = "staging"
  }
  common_tags = {
    "managedBy"          = "DevOps"
    "solutionOwner"      = "RDO"
    "activityName"       = "Storage Account"
    "dataClassification" = "Internal"
    "automation"         = ""
    "costCentre"         = ""
  }
  enforced_tags = module.tags.common_tags
}




