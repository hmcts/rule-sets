output "common_tags" {
  value = {
    Environment = var.env
    Product     = var.product
    BuiltFrom   = var.builtFrom
  }
}

output "included_repositories" {
  value = local.included_repositories
}

output "repo_branch_combinations" {
  value = local.repo_branch_combinations
}
