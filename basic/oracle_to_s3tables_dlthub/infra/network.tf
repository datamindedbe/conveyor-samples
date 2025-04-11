locals {
  vpc_id      = "vpc-0cc4cd37c991fff9c"
  oliver_home = "176.6.128.0/20" # based on three IPs obtained. Allows 2k addresses
  siyan_home  = "91.176.58.65/32"
  allowed_ips = [local.oliver_home, local.siyan_home]
}

data "aws_availability_zones" "available_zones" {}

resource "aws_security_group" "test_security_group" {
  name        = "oracle-rds"
  description = "to allow connections to this RDS instance"
  vpc_id      = local.vpc_id
}

resource "aws_vpc_security_group_ingress_rule" "allow_tls_ipv4" {
  for_each          = toset(local.allowed_ips)
  security_group_id = aws_security_group.test_security_group.id
  cidr_ipv4         = each.key
  from_port         = 443
  ip_protocol       = "tcp"
  to_port           = 443
}

resource "aws_vpc_security_group_ingress_rule" "allow_oracle_clients" {
  for_each          = toset(local.allowed_ips)
  security_group_id = aws_security_group.test_security_group.id
  cidr_ipv4         = each.key
  from_port         = 1521
  ip_protocol       = "tcp"
  to_port           = 1521
}

resource "aws_vpc_security_group_ingress_rule" "allow_ping" {
  for_each          = toset(local.allowed_ips)
  security_group_id = aws_security_group.test_security_group.id
  cidr_ipv4         = each.key
  from_port         = 8
  ip_protocol       = "icmp"
  to_port           = 8
}

resource "aws_vpc_security_group_egress_rule" "allow_tls_ipv6" {
  count             = 1
  security_group_id = aws_security_group.test_security_group.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv6" {
  count             = 1
  security_group_id = aws_security_group.test_security_group.id
  cidr_ipv6         = "::/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}

resource "aws_db_subnet_group" "database_subnet_group" {
  name        = "oracle-subnet"
  subnet_ids  = ["subnet-074a20fad3e957d2f", "subnet-0935e3a4721c029df"]
  description = "oracle-subnet"
}
