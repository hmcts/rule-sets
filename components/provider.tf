# provider "github" {
#   token = var.github_token
#   owner = "hmcts"
# }

terraform {
  required_version = ">= 1.3.6"

  #   backend "azurerm" {
  #   }
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.109.0"
    }
  }
}

provider "azurerm" {
  features {}
}

terraform {
  backend "azurerm" {
    resource_group_name   = "rule-set-rg"
    storage_account_name  = "rulesetsa"
    container_name        = "tfstate"
    key                   = "terraform.tfstate"
  }
}