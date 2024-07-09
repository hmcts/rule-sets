locals {
  # Read the repositories list from the JSON file
  repositories_list = jsondecode(file("${path.module}/../production-repos.json"))

  # Filter out excluded repositories
  included_repositories = [
    for repo in local.repositories_list : repo
    if !contains(var.excluded_repositories, repo)
  ]

  # Create a combination of repositories and branches
  repo_branch_combinations = flatten([
    for repo in local.included_repositories : [
      for branch in var.branches : {
        repo   = repo
        branch = branch
      }
    ]
  ])
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




