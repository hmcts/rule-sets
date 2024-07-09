module "tags" {
  source      = "git::https://github.com/hmcts/terraform-module-common-tags.git?ref=master"
  environment = var.env
  product     = var.product
  builtFrom   = var.builtFrom
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
  tags     = module.tags.common_tags
}

resource "azurerm_storage_account" "sa" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  tags                     = module.tags.common_tags
}

resource "azurerm_storage_container" "tfstate" {
  name                  = "tfstate"
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "private"
}

# Check if repositories exist
data "github_repository" "existing_repos" {
  for_each = { for repo in local.included_repositories : repo => repo }
  name     = each.key
}

# Check if branches exist
data "github_branch" "existing_branches" {
  for_each   = { for combo in local.repo_branch_combinations : "${combo.repo}:${combo.branch}" => combo if contains(keys(data.github_repository.existing_repos), combo.repo) }
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
  enforce_admins = false

  required_status_checks {
    strict   = true
    contexts = ["ci/test", "ci/lint"]
  }

  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = false
    required_approving_review_count = 1
  }

  restrictions {
    users = []
    teams = []
    apps  = []
  }
}
