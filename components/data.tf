data "github_team" "admin"{
  slug = "Platform Operations"
}

data "local_file" "repos_json" {
  filename = "${path.module}./production-repos.json"
}

data "github_branch" "existing_branches" {
  for_each = {
    for combo in local.repo_branch_combinations : "${combo.repo}:${combo.branch}" => combo
  }
  repository = each.value.repo
  branch     = each.value.branch
}