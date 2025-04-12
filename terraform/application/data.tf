data "terraform_remote_state" "common" {
  backend = "s3"

  config = {
    bucket = local.tfstate_bucket_name
    key    = "common/terraform.tfstate"
    region = local.region
  }
}


data "aws_ami" "al2023" {
  most_recent = true

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["137112412989"] # Amazon 공식 계정 ID
}
 
