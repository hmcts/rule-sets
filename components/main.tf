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


locals {
  existing_branches = {
    for branch in data.github_branch.existing_branches :
    "${branch.repository}:${branch.branch}" => branch
    if branch.branch != null
  }

  branch_summary = {
    for repo in local.included_repositories :
    repo => {
      main   = contains(keys(local.existing_branches), "${repo}:main")
      master = contains(keys(local.existing_branches), "${repo}:master")
    }
  }
}

resource "github_branch_protection_v3" "branch_protection" {
  for_each = local.existing_branches

  repository                      = each.value.repository
  branch                          = each.value.branch
  enforce_admins                  = false
  require_signed_commits          = false
  require_conversation_resolution = false

  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = false
    required_approving_review_count = 1
  }

  required_status_checks {
    contexts = ["ci/lint", "ci/test"]
    strict   = true
  }

  restrictions {
    users = []
    teams = []
    apps  = []
  }
}