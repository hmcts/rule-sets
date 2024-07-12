locals {
  included_repositories = jsondecode(data.local_file.repos_json.content)
  branches_to_check     = ["main", "master"]
  batch_size            = 20

  # Split repositories into batches of 20
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

# Create a map of existing branches, then iterates over the github_branch data source results 
locals {
  existing_branches = {
    for branch in data.github_branch.existing_branches :
    "${branch.repository}:${branch.branch}" => branch
    if branch.branch != null
  }

  #Checks if a main/master branch exists on the repositorys

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




