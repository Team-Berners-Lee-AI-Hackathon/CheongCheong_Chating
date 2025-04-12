output "pdf_info_stream_arn" {
  value = aws_dynamodb_table.pdf_info.stream_arn
}

output "pdf_bucket_id" {
  value = aws_s3_bucket.pdf_bucket.id
}