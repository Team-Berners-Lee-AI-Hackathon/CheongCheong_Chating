resource "aws_dynamodb_table" "user_info" {
  name         = "${local.pjt}-user-info-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }

}