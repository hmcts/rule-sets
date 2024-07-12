data "github_repository" "repos" {
  for_each = toset(local.included_repositories)
  name     = each.value
}

data "github_branch" "existing_branches" {
  for_each = {
    for combo in local.repo_branch_combinations :
    "${combo.repo}:${combo.branch}" => combo
  }
  depends_on = [time_sleep.wait_for_repo_data]

  repository = each.value.repo
  branch     = each.value.branch
}

data "local_file" "repos_json" {
  filename = "${path.module}./production-repos.json"
}