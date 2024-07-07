provider "azurerm" {
  features {}
}

provider "github" {
  owner = "hmcts"
  token = var.github_token
}

terraform {
  required_version = ">= 1.4.0"

  backend "azurerm" {
    resource_group_name  = "rule-set-rg"
    storage_account_name = "rulesetsa"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
    use_oidc             = true
    use_azuread_auth     = true
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.109.0"
    }
  }
}
