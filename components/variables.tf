# variable "github_token" {
#   description = "GitHub token to use for authentication."
#   type        = string
#   sensitive   = true
# }

variable "branches" {
  description = "List of branches to apply protection rules"
  type        = list(string)
  default = [
    "master",
    "main"
  ]
}

variable "excluded_repositories" {
  description = "List of repositories to exclude from branch protection rules"
  type        = list(string)
  default = [
    # "rule-set-test-repo5"
    # "rule-set-test-repo7",
    "rule-set-test-repo8"
  ]
}

variable "override_action" {
  description = "The action to override"
  type        = string
  default     = "plan"
}

variable "location" {
  description = "The location for the resources"
  type        = string
  default     = "UK South"
}

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "rule-set-rg"
}

variable "storage_account_name" {
  description = "The name of the storage account"
  type        = string
  default     = "rulesetsa"
}

variable "env" {
  description = "The environment for the deployment (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "product" {
  description = "The product name or identifier"
  type        = string
  default     = "sds-platform"
}

variable "builtFrom" {
  description = "Information about the build source or version"
  type        = string
  default     = "https://github.com/hmcts/github-repository-rules"
}