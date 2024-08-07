provider "azurerm" {
  features {}
}

provider "github" {
  owner = "hmcts-test"
  token = var.oauth_token
}

terraform {
  required_version = ">= 1.5.7"

  backend "azurerm" {
    resource_group_name  = "rule-set-rg"
    storage_account_name = "rulesetsa"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
    use_oidc             = true
    use_azuread_auth     = true
  }
}

terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }
}
