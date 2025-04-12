
locals {
  pjt    = "ai-hackerthon"
  region = "ap-northeast-2"

  pdf_info_table_name = "${local.pjt}-pdf-info-table"
  pdf_bucket_id = "${local.pjt}-pdf-bucket"

  pdf_processor_zip = "${path.module}/functions/pdf_processor/dst/lambda_function.zip"
  notifier_zip      = "${path.module}/functions/notifier/dst/lambda_function.zip"
}   