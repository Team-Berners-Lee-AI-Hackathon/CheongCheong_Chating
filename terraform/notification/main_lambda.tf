#########################################################
# pdf 프로세싱 람다
#########################################################

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

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = data.terraform_remote_state.backing.outputs.pdf_bucket_id
  lambda_function {
    lambda_function_arn = aws_lambda_function.pdf_processor.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".pdf"
  }
}

resource "aws_lambda_event_source_mapping" "dynamodb_stream" {
  event_source_arn  = data.terraform_remote_state.backing.outputs.pdf_info_stream_arn
  function_name     = aws_lambda_function.notifier.arn
  starting_position = "LATEST"

  batch_size                         = 1
  maximum_batching_window_in_seconds = 10
}

#########################################################
# notification 람다
#########################################################
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

