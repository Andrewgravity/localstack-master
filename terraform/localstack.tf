resource "aws_s3_bucket" "my-bucket" {
  bucket = "my-bucket"
}

resource "aws_dynamodb_table" "my-raw-table" {
  name           = "my_raw_table"
  read_capacity  = var.dynamodb.capacity.read
  write_capacity = var.dynamodb.capacity.write
  hash_key       = "departure_id"
  range_key      = "return_id"
  attribute {
    name = "departure_id"
    type = "N"
  }
  attribute {
    name = "return_id"
    type = "N"
  }
}

resource "aws_dynamodb_table" "my-metrics-table" {
  name           = "my_metrics_table"
  read_capacity  = var.dynamodb.capacity.read
  write_capacity = var.dynamodb.capacity.write
  hash_key       = "name"
  attribute {
    name = "name"
    type = "S"
  }
}

resource "aws_dynamodb_table" "my-daily-metrics-table" {
  name           = "my_daily_metrics_table"
  read_capacity  = var.dynamodb.capacity.read
  write_capacity = var.dynamodb.capacity.write
  hash_key       = "date"
  attribute {
    name = "date"
    type = "S"
  }
}

resource "aws_dynamodb_table" "my-monthly-metrics-table" {
  name           = "my_monthly_metrics_table"
  read_capacity  = var.dynamodb.capacity.read
  write_capacity = var.dynamodb.capacity.write
  hash_key       = "date"
  attribute {
    name = "date"
    type = "S"
  }
}

resource "aws_sqs_queue" "my-queue" {
  name = "my-queue"
}

resource "aws_sns_topic" "my-topic" {
  name = "my-topic"
}

resource "aws_lambda_function" "load-file-to-raw-table-lambda" {
  function_name = "load_file_to_raw_table"
  role          = var.lambda.role
  handler       = "load_file_to_raw_table.lambda_handler"
  filename      = "${var.lambda.directory}/load_file_to_raw_table.zip"
  runtime       = var.lambda.runtime
  timeout       = var.lambda.timeout
  environment {
    variables = {
      AWS_ENDPOINT_URL = var.aws.endpoint.lambda
      AWS_ACCESS_KEY   = var.aws.access_key
      AWS_SECRET_KEY   = var.aws.secret_key
      AWS_REGION_NAME  = var.aws.region
    }
  }
}

resource "aws_lambda_function" "load-file-to-metrics-table-lambda" {
  function_name = "load_file_to_metrics_table"
  role          = var.lambda.role
  handler       = "load_file_to_metrics_table.lambda_handler"
  filename      = "${var.lambda.directory}/load_file_to_metrics_table.zip"
  runtime       = var.lambda.runtime
  timeout       = var.lambda.timeout
  environment {
    variables = {
      AWS_ENDPOINT_URL = var.aws.endpoint.lambda
      AWS_ACCESS_KEY   = var.aws.access_key
      AWS_SECRET_KEY   = var.aws.secret_key
      AWS_REGION_NAME  = var.aws.region
    }
  }
}

resource "aws_lambda_function" "load-file-to-daily-metrics-table-lambda" {
  function_name = "load_file_to_daily_metrics_table"
  role          = var.lambda.role
  filename      = "${var.lambda.directory}/load_file_to_daily_metrics_table.zip"
  handler       = "load_file_to_daily_metrics_table.lambda_handler"
  runtime       = var.lambda.runtime
  timeout       = var.lambda.timeout
  environment {
    variables = {
      AWS_ENDPOINT_URL = var.aws.endpoint.lambda
      AWS_ACCESS_KEY   = var.aws.access_key
      AWS_SECRET_KEY   = var.aws.secret_key
      AWS_REGION_NAME  = var.aws.region
    }
  }
}

resource "aws_lambda_function" "load-file-to-monthly-metrics-table-lambda" {
  function_name = "load_file_to_monthly_metrics_table"
  role          = var.lambda.role
  filename      = "${var.lambda.directory}/load_file_to_monthly_metrics_table.zip"
  handler       = "load_file_to_monthly_metrics_table.lambda_handler"
  runtime       = var.lambda.runtime
  timeout       = var.lambda.timeout
  environment {
    variables = {
      AWS_ENDPOINT_URL = var.aws.endpoint.lambda
      AWS_ACCESS_KEY   = var.aws.access_key
      AWS_SECRET_KEY   = var.aws.secret_key
      AWS_REGION_NAME  = var.aws.region
    }
  }
}

resource "aws_s3_bucket_notification" "object-created-notification" {
  bucket = aws_s3_bucket.my-bucket.bucket
  queue {
    queue_arn     = aws_sqs_queue.my-queue.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = "metrics"
    filter_suffix = ".csv"
  }
  topic {
    topic_arn     = aws_sns_topic.my-topic.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = "data"
    filter_suffix = ".csv"
  }
}

resource "aws_lambda_event_source_mapping" "s3-metrics-object-created-event-load-file-to-metrics-table-lambda-mapping" {
  function_name    = aws_lambda_function.load-file-to-metrics-table-lambda.arn
  event_source_arn = aws_sqs_queue.my-queue.arn
}

resource "aws_sns_topic_subscription" "s3-object-created-notification-load-file-to-raw-table-lambda-subscription" {
  topic_arn = aws_sns_topic.my-topic.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.load-file-to-raw-table-lambda.arn
}

resource "aws_sns_topic_subscription" "s3-object-created-notification-load-file-to-daily-metrics-table-lambda-subscription" {
  topic_arn = aws_sns_topic.my-topic.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.load-file-to-daily-metrics-table-lambda.arn
}

resource "aws_sns_topic_subscription" "s3-object-created-notification-load-file-to-monthly-metrics-table-lambda-subscription" {
  topic_arn = aws_sns_topic.my-topic.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.load-file-to-monthly-metrics-table-lambda.arn
}
