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
  # Read the repositories from the JSON file
  repositories_json = file("${path.module}./test-repos.json")
  repositories_data = jsondecode(local.repositories_json)

  # Create combinations of repositories and branches
  repo_branch_combinations = flatten([
    for repo in local.repositories_data : [
      for branch in var.branches : {
        repo   = repo
        branch = branch
      }
    ]
  ])
}