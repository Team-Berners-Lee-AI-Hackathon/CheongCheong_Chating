locals {
  pdf_processor_zip = "${path.module}/functions/pdf_processor/dst/lambda_function.zip"
  notifier_zip      = "${path.module}/functions/notifier/dst/lambda_function.zip"
}

data "archive_file" "pdf_processor" {
  type        = "zip"
  source_dir  = "${path.module}/functions/pdf_processor/src"
  output_path = local.pdf_processor_zip
}

resource "aws_lambda_function" "pdf_processor" {
  filename         = local.pdf_processor_zip
  function_name    = "${local.pjt}-pdf-processor"
  role             = aws_iam_role.pdf_processor_lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256("${data.archive_file.pdf_processor.source_dir}/lambda_function.py")

  environment {
    variables = {
      TABLE_NAME = local.pdf_info_table_name
    }
  }

  depends_on = [
    data.archive_file.pdf_processor
  ]
}

resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pdf_processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.pdf_bucket.arn
}

data "archive_file" "notifier" {
  type        = "zip"
  source_dir  = "${path.module}/functions/notifier/src"
  output_path = local.notifier_zip
}

resource "aws_lambda_function" "notifier" {
  filename         = local.notifier_zip
  function_name    = "${local.pjt}-notifier"
  role             = aws_iam_role.notifier_lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256("${data.archive_file.notifier.source_dir}/lambda_function.py")

  depends_on = [
    data.archive_file.notifier
  ]
}

resource "aws_lambda_event_source_mapping" "dynamodb_stream" {
  event_source_arn  = aws_dynamodb_table.pdf_info.stream_arn
  function_name     = aws_lambda_function.notifier.arn
  starting_position = "LATEST"

  batch_size                         = 1
  maximum_batching_window_in_seconds = 10
}
