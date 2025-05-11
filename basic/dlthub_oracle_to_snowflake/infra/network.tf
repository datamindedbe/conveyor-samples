data "aws_availability_zones" "available_zones" {}

resource "aws_security_group" "test_security_group" {
  name        = "oracle-rds"
  description = "to allow connections to this RDS instance"
  vpc_id      = var.vpc_id
}

resource "aws_vpc_security_group_ingress_rule" "allow_oracle_clients" {
  security_group_id = aws_security_group.test_security_group.id
  cidr_ipv4         = "0.0.0.0/0" # each.key
  from_port         = var.db_port
  ip_protocol       = "tcp"
  to_port           = var.db_port
}

resource "aws_vpc_security_group_egress_rule" "allow_tls_ipv4" {
  count             = 1
  security_group_id = aws_security_group.test_security_group.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv6" {
  count             = 1
  security_group_id = aws_security_group.test_security_group.id
  cidr_ipv6         = "::/0"
  ip_protocol       = "-1"
}

resource "aws_db_subnet_group" "database_subnet_group" {
  name        = "oracle-subnet"
  subnet_ids  = [var.db_subnet]
  description = "oracle-subnet"
}
