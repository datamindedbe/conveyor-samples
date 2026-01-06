data "conveyor_environment" "dev3" {
  name = "dev3"
}

resource "conveyor_project" "pi_spark" {
  name           = "pi_spark"
  git_repo       = "https://github.com/datamindedbe/conveyor-samples"
  git_sub_folder = "basic/pi_spark"
  default_ide_environment_id = data.conveyor_environment.dev3.id


  default_ide_config {
    build_steps {
      name = "setup env"
      cmd  = <<EOF
sudo apt update
sudo apt install make openjdk-11-jre gcc libbz2-dev openssl\
  libncurses5-dev libncursesw5-dev libssl-dev libreadline-dev liblzma-dev libsqlite3-dev -y
EOF
    }
  }
}

