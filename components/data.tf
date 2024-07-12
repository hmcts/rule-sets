data "github_repository" "repos" {
  for_each = toset(local.included_repositories)
  name     = each.value
}

data "github_branch" "existing_branches" {
  count = length(local.repo_branch_combinations)

  repository = local.repo_branch_combinations[count.index].repo
  branch     = local.repo_branch_combinations[count.index].branch
}

data "local_file" "repos_json" {
  filename = "${path.module}./prod-repos.json"
}