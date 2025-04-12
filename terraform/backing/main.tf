resource "aws_dynamodb_table" "pdf_info" {
  name         = local.pdf_info_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  stream_enabled   = true
  stream_view_type = "NEW_IMAGE"
}


resource "aws_dynamodb_table" "user_info" {
  name         = "${local.pjt}-user-info-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }

}