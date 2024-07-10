output "common_tags" {
  value = {
    Environment = var.env
    Product     = var.product
    BuiltFrom   = var.builtFrom
  }
}

# output "branch_summary" {
#   value = {
#     for repo, branches in local.branch_summary :
#     repo => branches
#     if branches.main && branches.master  # This will only show repos with both main and master
#   }
#   description = "Repositories that have both 'main' and 'master' branches"
# }

output "branch_count" {
  value = {
    total_repos = length(local.included_repositories)
    repos_with_main = sum([for repo, branches in local.branch_summary : branches.main ? 1 : 0])
    repos_with_master = sum([for repo, branches in local.branch_summary : branches.master ? 1 : 0])
    repos_with_both = sum([for repo, branches in local.branch_summary : (branches.main && branches.master) ? 1 : 0])
  }
  description = "Summary of branch counts"
}