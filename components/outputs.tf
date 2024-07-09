output "common_tags" {
  value = {
    Environment = var.env
    Product     = var.product
    BuiltFrom   = var.builtFrom
  }
}

output "raw_repositories_list" {
  value = local.raw_repositories_list
}

output "repositories_list" {
  value = local.repositories_list
}

output "included_repositories" {
  value = local.included_repositories
}

output "repo_branch_combinations" {
  value = local.repo_branch_combinations
}