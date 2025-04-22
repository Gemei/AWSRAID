import boto3
import modules.globals as my_globals
from botocore import UNSIGNED
from botocore.client import Config

def initialize_aws_unsigned_s3_client():
    my_globals.unsigned_s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))

def initialize_aws_victim_clients(victim_access_key, victim_secret_access_key, victim_session_token, victim_region):
    if victim_access_key is not None and victim_secret_access_key is not None:
        victim_session = boto3.Session(
            aws_access_key_id=victim_access_key,
            aws_secret_access_key=victim_secret_access_key,
            aws_session_token=victim_session_token
        )
        victim_clients = {
            "sts_client": victim_session.client("sts"),
            "iam_client": victim_session.client("iam"),
            "s3_client": victim_session.client("s3"),
            "secrets_manager_client": victim_session.client("secretsmanager", region_name=victim_region),
            "ec2_client": victim_session.client("ec2", victim_region),
            "lambda_client": victim_session.client("lambda", victim_region, config=Config(read_timeout=10, connect_timeout=10)),
            "rds_client": victim_session.client("rds", victim_region),
            "cognito_client": victim_session.client("cognito-idp", victim_region),
            "macie_client": victim_session.client("macie2", victim_region),
            "ssm_client": victim_session.client("ssm", victim_region),
            "elastic_beanstalk_client": victim_session.client("elasticbeanstalk", victim_region),
            "sqs_client": victim_session.client("sqs", victim_region),
            "code_commit_client": victim_session.client("codecommit", victim_region)
        }
        return victim_session, victim_clients
    else:
        return None, None

def initialize_aws_attacker_clients(attacker_access_key, attacker_secret_access_key, attacker_region):
    if attacker_access_key is not None and attacker_secret_access_key is not None:
        attacker_session = boto3.Session(
            aws_access_key_id=attacker_access_key,
            aws_secret_access_key=attacker_secret_access_key
        )
        attacker_clients = {
            "sts_client": attacker_session.client("sts"),
            "iam_client": attacker_session.client("iam"),
            "s3_client": attacker_session.client("s3"),
            "secrets_manager_client": attacker_session.client("secretsmanager", region_name=attacker_region),
            "ec2_client": attacker_session.client("ec2", attacker_region),
            "lambda_client": attacker_session.client("lambda", attacker_region, config=Config(read_timeout=10, connect_timeout=10)),
            "rds_client": attacker_session.client("rds", attacker_region),
            "cognito_client": attacker_session.client("cognito-idp", attacker_region),
            "macie_client": attacker_session.client("macie2", attacker_region),
            "ssm_client": attacker_session.client("ssm", attacker_region),
            "elastic_beanstalk_client": attacker_session.client("elasticbeanstalk", attacker_region),
            "sqs_client": attacker_session.client("sqs", attacker_region),
            "code_commit_client": attacker_session.client("codecommit", attacker_region)
        }
        return attacker_session, attacker_clients
    return None, None