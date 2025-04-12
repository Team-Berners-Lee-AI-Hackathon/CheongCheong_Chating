data "archive_file" "pdf_processor" {
  type        = "zip"
  source_dir  = "${path.module}/functions/pdf_processor/src"
  output_path = local.pdf_processor_zip
}

data "archive_file" "notifier" {
  type        = "zip"
  source_dir  = "${path.module}/functions/notifier/src"
  output_path = local.notifier_zip
}

data "terraform_remote_state" "backing" {
  backend = "s3"

  config = {
    bucket = local.tfstate_bucket_name
    key    = "common/terraform.tfstate"
    region = local.region
  }
}
