terraform {
  required_version = ">= 1.5.0"
  backend "azurerm" {} // When using remote
  #backend "local" {} // When using local
}

terraform {
  required_version = ">= 1.8.0, < 1.9.0"
}

provider "azurerm" {
  features {}
}