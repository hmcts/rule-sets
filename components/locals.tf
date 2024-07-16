locals {
  # List of repositories to exclude from having the rule sets applied to
  excluded_repositories = [
    "test-repo-uteppyig",
    "test-repo-1ew34nh9",
  ]

  # Read repositories from production-repos.json file 
  all_repositories = jsondecode(file("./production-repos.json"))

  # Filter out excluded repositories
  included_repositories = [
    for repo in local.all_repositories : repo
    if !contains(local.excluded_repositories, repo)
  ]

  branches_to_check = ["main", "master"]

  branch_summary = {
    for repo in local.included_repositories :
    repo => {
      main   = contains(local.branches_to_check, "main")
      master = contains(local.branches_to_check, "master")
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




