# locals {
#   // List of included repositories, taken directly from the 'repositories' variable
#   included_repositories = var.repositories

#   // Create combinations of repositories and branches by flattening a nested loop
#   repo_branch_combinations = flatten([
#     // Iterate over each repository in the included_repositories list
#     for repo in local.included_repositories : [
#       // For each repository, iterate over each branch in the 'branches' variable
#       for branch in var.branches : {
#         // Create a map with the repository and branch names
#         repo   = repo
#         branch = branch
#       }
#     ]
#   ])
# }

locals {
  # Read the repositories list from the JSON file
  repositories_list = jsondecode(file("${path.module}/../test-repos.json"))

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




