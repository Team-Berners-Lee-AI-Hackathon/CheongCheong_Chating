resource "aws_iam_role" "pdf_processor_lambda_role" {
  name = "${local.pjt}-pdf-processor-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role" "notifier_lambda_role" {
  name = "${local.pjt}-notifier-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "pdf_role_lambda_basic" {
  role       = aws_iam_role.pdf_processor_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "notifier_role_lambda_basic" {
  role       = aws_iam_role.notifier_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "pdf_lambda" {
  name = "${local.pjt}-pdf-lambda-policy"
  role = aws_iam_role.pdf_processor_lambda_role.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
        
        ]
        Resource = [
          aws_s3_bucket.pdf_bucket.arn,
          "${aws_s3_bucket.pdf_bucket.arn}/*"
        ]
      },
            {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
        ]
        Resource = [
          "*"
        ]
      }
      
    ]
  })
}


resource "aws_iam_role_policy" "notifier_lambda" {
  name = "${local.pjt}-notifier-lambda-policy"
  role = aws_iam_role.notifier_lambda_role.name
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:GetItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWriteItem",
          "dynamodb:DescribeStream",
          "dynamodb:GetRecords",
          "dynamodb:GetShardIterator",
          "dynamodb:ListStreams"
        ]
        Resource = [
          "arn:aws:dynamodb:${local.region}:*:table/${local.pjt}-*"
        ]
      }
    ]
  })
}
