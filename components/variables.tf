variable "github_token" {
  description = "GitHub token to use for authentication."
  type        = string
  sensitive   = true
}

# variable "repositories" {
#   description = "List of repositories to apply branch protection rules"
#   type        = list(string)
#   default     = [
#     "rule-set-test-repo",
#     "rule-set-test-repo1",
#     "rule-set-test-repo2"
#   ]
# }

variable "branches" {
  description = "List of branches to apply protection rules"
  type        = list(string)
  default     = [
    "master",
    "main"
  ]
}

variable "excluded_repositories" {
  description = "List of repositories to exclude from branch protection rules"
  type        = list(string)
  default     = [
    "repo-to-exclude"
  ]
}

variable "override_action" {
  description = "The action to override"
  type        = string
}

variable "location" {
  description = "The location for the resources"
  type        = string
}
