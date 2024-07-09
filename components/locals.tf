locals {
  raw_repositories_list = jsondecode(file("${path.module}/../production-repos.json"))

  # Extract repository names and ensure uniqueness
  repositories_list = distinct([
    for repo in local.raw_repositories_list :
    regex("[a-zA-Z0-9-_/]+", replace(repo, "^https://github.com/(.*?)(?:\\.git)?(?:\\?.*)?$", "$1"))
  ])

  included_repositories = local.repositories_list

  repo_branch_combinations = flatten([
    for repo in local.included_repositories : [
      for branch in ["master", "main"] : {
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




