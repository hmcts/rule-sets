output "common_tags" {
  value = {
    Environment = var.env
    Product     = var.product
    BuiltFrom   = var.builtFrom
  }
}