provider "aws" {
    region = "ap-southeast-1"
}

data "archive_file" "lambda_zip" {
    type          = "zip"
    source_file   = "price_change_lambda_func.py"
    output_path   = "lambda_function.zip"
}

resource "aws_lambda_function" "analysePriceChange" {
    memory_size      = "128"
    timeout          = "30"
    filename         = "lambda_function.zip"
    function_name    = "analysePriceChange"
    role             = "${aws_iam_role.iam_for_lambda_tf.arn}"
    handler          = "analyse_price_change.lambda_handler"
    source_code_hash = "${data.archive_file.lambda_zip.output_base64sha256}"
    runtime          = "python3.6"
}

resource "aws_iam_role" "iam_for_lambda_tf" {
    name = "iam_for_lambda_tf"

    assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
        },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
EOF
}