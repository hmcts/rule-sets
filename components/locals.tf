locals {
  # List of repositories to exclude from the production-repos.json file
  excluded_repositories = [] # Add any repositories here you would like to exclude

  # Read repositories from JSON file
  all_repositories = jsondecode(data.local_file.repos_json.content)

  # Filter out excluded repos
  included_repositories = [
    for repo in local.all_repositories : repo
    if !contains(local.excluded_repositories, repo)
  ]
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