resource "aws_instance" "app_server" {
    ami                         = data.aws_ami.al2023.id
    instance_type               = "t2.micro"
    subnet_id                   = data.terraform_remote_state.common.outputs.public_subnets[0]
    associate_public_ip_address = true
    iam_instance_profile         = aws_iam_instance_profile.ec2_instance_profile.name

    tags = {
      Name = "AppServer"
    }
  }

resource "aws_iam_role" "ec2_role" {
    name = "ec2-app-role"

    assume_role_policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Effect = "Allow",
          Principal = {
            Service = "ec2.amazonaws.com"
          },
          Action = "sts:AssumeRole"
        }
      ]
    })
}

resource "aws_iam_policy" "ec2_dynamodb_s3_access" {
    name        = "EC2DynamoDBS3Access"
    description = "Allow EC2 instance to access DynamoDB and S3"

    policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Effect = "Allow",
          Action = [
            "dynamodb:*",
            "s3:*"
          ],
          Resource = "*"
        }
      ]
    })
}

resource "aws_iam_role_policy_attachment" "attach_policy" {
    role       = aws_iam_role.ec2_role.name
    policy_arn = aws_iam_policy.ec2_dynamodb_s3_access.arn
}

resource "aws_iam_instance_profile" "ec2_instance_profile" {
    name = "ec2-app-instance-profile"
    role = aws_iam_role.ec2_role.name
}