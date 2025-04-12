resource "aws_instance" "app_server" {
    ami                         = data.aws_ami.al2023.id
    instance_type               = "t2.micro"
    subnet_id                   = data.terraform_remote_state.common.outputs.public_subnets[0]
    associate_public_ip_address = true

    tags = {
      Name = "AppServer"
    }
  }