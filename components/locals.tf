locals {
  included_repositories = jsondecode(data.local_file.repos_json.content)
  branches_to_check     = ["main", "master"]
  batch_size            = 10
  
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

# Fetch existing branches for each repository
data "github_branch" "existing_branches" {
  for_each = {
    for combo in local.repo_branch_combinations : "${combo.repo}:${combo.branch}" => combo
  }
  
  repository = each.value.repo
  branch     = each.value.branch
}

# Create a map of existing branches
locals {
  existing_branches = {
    for key, branch in data.github_branch.existing_branches :
    key => branch
    if branch.name != null
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




