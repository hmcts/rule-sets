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

output "valid_branch_combinations" {
  value = {
    for combo in local.repo_branch_combinations : "${combo.repo}:${combo.branch}" => combo
    if try(data.github_branch.existing_branches["${combo.repo}:${combo.branch}"].branch, null) != null
  }
}

