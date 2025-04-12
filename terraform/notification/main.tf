resource "aws_s3_bucket" "pdf_bucket" {
  bucket = "${local.pjt}-pdf-bucket"
}


resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.pdf_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.pdf_processor.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".pdf"
  }

}

