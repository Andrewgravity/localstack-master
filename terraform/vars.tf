variable "aws" {
  type = object({
    access_key = string
    secret_key = string
    region     = string
    endpoint   = map(string)
  })
  default = {
    access_key = "test"
    secret_key = "test"
    region     = "us-east-1"
    endpoint = {
      lambda   = "http://localhost:4566"
      iam      = "http://localhost:4566"
      s3       = "http://localhost:4566"
      sqs      = "http://localhost:4566"
      sns      = "http://localhost:4566"
      dynamodb = "http://localhost:4566"
    }
  }
}

variable "dynamodb" {
  type = object({
    capacity = map(number)
  })
  default = {
    capacity = {
      read  = 10
      write = 10
    }
  }
}

variable "lambda" {
  type = object({
    directory = string
    role      = string
    runtime   = string
    timeout   = number
  })
  default = {
    directory = "../lambda-src"
    role      = "mock_role"
    runtime   = "python3.9"
    timeout   = 900
  }
}