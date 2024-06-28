variable "location" {
  type        = string
  default     = "UK South"
  description = "Location"
}

variable "rg_name" {
  type    = string
  default = "test-rg-soc"
}

variable "env" {
  description = "The environment for the deployment (e.g., dev, staging, prod)"
  type        = string
}

variable "product" {
  description = "The product name or identifier"
  type        = string
}

variable "builtFrom" {
  description = "Information about the build source or version"
  type        = string
}