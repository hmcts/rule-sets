# Check if branches exist
data "github_branch" "existing_branches" {
  for_each   = { for combo in local.repo_branch_combinations : "${combo.repo}:${combo.branch}" => combo }
  repository = each.value.repo
  branch     = each.value.branch
}

# Apply branch protection rules only if the branch exists
resource "github_branch_protection_v3" "branch_protection" {
  for_each = {
    for combo in local.repo_branch_combinations : "${combo.repo}:${combo.branch}" => combo
    if try(data.github_branch.existing_branches["${combo.repo}:${combo.branch}"].branch, null) != null
  }

  repository     = each.value.repo
  branch         = each.value.branch
  enforce_admins = false  # Excludes organisation admins

  required_status_checks {
    strict   = true
    contexts = ["ci/test", "ci/lint"]
  }

  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = false
    required_approving_review_count = 2  # Ensure at least 1 reviewer
  }

  restrictions {
    users = []
    teams = []
    apps  = []
  }
}

output "existing_branches" {
  value = data.github_branch.existing_branches
}