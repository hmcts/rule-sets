locals {
  included_repositories = jsondecode(data.local_file.repos_json.content)
  branches_to_check     = ["main", "master"]
  batch_size            = 20

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

  existing_branches = {
    for key, branch in data.github_branch.existing_branches :
    key => branch
    if branch.branch != null
  }

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




