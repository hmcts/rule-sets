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

# resource "github_organization_ruleset" "default_ruleset" {
#   name        = local.org_ruleset.name
#   target      = local.org_ruleset.target
#   enforcement = local.org_ruleset.enforcement

#   conditions {
#     repository_name {
#       include = local.included_repositories
#       exclude = []
#     }
#     ref_name {
#       include = local.org_ruleset.conditions.ref_name.include
#       exclude = local.org_ruleset.conditions.ref_name.exclude
#     }
#   }

#   rules {
#     creation                = local.org_ruleset.rules.creation
#     update                  = local.org_ruleset.rules.update
#     deletion                = local.org_ruleset.rules.deletion
#     required_linear_history = local.org_ruleset.rules.required_linear_history

#     pull_request {
#       dismiss_stale_reviews_on_push     = local.org_ruleset.rules.pull_request.dismiss_stale_reviews_on_push
#       require_code_owner_review         = local.org_ruleset.rules.pull_request.require_code_owner_review
#       required_approving_review_count   = local.org_ruleset.rules.pull_request.required_approving_review_count
#       require_last_push_approval        = local.org_ruleset.rules.pull_request.require_last_push_approval
#       required_review_thread_resolution = local.org_ruleset.rules.pull_request.required_review_thread_resolution
#     }

#     required_status_checks {
#       strict_required_status_checks_policy = local.org_ruleset.rules.required_status_checks.strict_required_status_checks_policy
#       dynamic "required_check" {
#         for_each = local.org_ruleset.rules.required_status_checks.required_checks
#         content {
#           context = required_check.value.context
#         }
#       }
#     }
#   }

#   bypass_actors {
#     actor_id    = data.github_organization.org.id
#     actor_type  = "OrganizationAdmin"
#     bypass_mode = "always"
#   }
# }
