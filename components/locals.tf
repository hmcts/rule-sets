locals {
  # List of repositories to exclude
  excluded_repositories = [
    "test-repo-uteppyig",
    "test-repo-1ew34nh9",
  ]

  # Read repositories from JSON file
  all_repositories = jsondecode(data.local_file.repos_json.content)

  # Filter out excluded repositories
  included_repositories = [
    for repo in local.all_repositories : repo
    if !contains(local.excluded_repositories, repo)
  ]

  branches_to_check = ["main", "master"]
  batch_size        = 10
  
  # Split repositories into batches of 10
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
}

# Create a map of existing branches
locals {
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
}

locals {
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




