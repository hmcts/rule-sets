output "common_tags" {
  value = {
    Environment = var.env
    Product     = var.product
    BuiltFrom   = var.builtFrom
  }
}


# This outout below will summarise how many repos have a master, main or both branches on the repos
output "branch_count" {
  value = {
    total_repos       = length(local.included_repositories)
    repos_with_main   = sum([for repo, branches in local.branch_summary : branches.main ? 1 : 0])
    repos_with_master = sum([for repo, branches in local.branch_summary : branches.master ? 1 : 0])
    repos_with_both   = sum([for repo, branches in local.branch_summary : (branches.main && branches.master) ? 1 : 0])
  }
  description = "Summary of branch counts"
}

# Output the clone URLs for each repository
output "repo_clone_urls" {
  value = github_repository.test_repo[*].http_clone_url
}