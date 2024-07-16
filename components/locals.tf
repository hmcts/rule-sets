locals {
  included_repositories = jsondecode(data.local_file.repos_json.content)
  branches_to_check     = ["main", "master"]

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




