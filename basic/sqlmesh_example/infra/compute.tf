resource "snowflake_warehouse" "warehouse" {
  name           = var.warehouse
  warehouse_size = "XSMALL"
  auto_suspend   = 60
  auto_resume    = true
}
