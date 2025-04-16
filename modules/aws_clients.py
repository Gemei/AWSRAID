import boto3
from botocore import UNSIGNED
from botocore.client import Config

def initialize_aws_clients(access_key, secret_access_key, session_token, region):
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token
    )
    clients = {
        "sts_client": session.client("sts"),
        "iam_client": session.client("iam"),
        "s3_client": session.client("s3"),
        "secrets_client": session.client("secretsmanager", region_name=region),
        "ec2_client": session.client("ec2", region),
        "lambda_client": session.client("lambda", region),
        "unsigned_s3_client": boto3.client("s3", config=Config(signature_version=UNSIGNED)),
        "rds_client": session.client("rds", region),
        "cognito_client": session.client("cognito-idp", region),
        "macie_client": session.client("macie2", region),
        "ssm_client": session.client("ssm", region),
        "elasticbeanstalk_client": session.client("elasticbeanstalk", region),
        "sqs_client": session.client("sqs", region)
    }
    return session, clients
