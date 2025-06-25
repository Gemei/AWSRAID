import boto3
import modules.globals as my_globals
from botocore import UNSIGNED
from botocore.client import Config

def initialize_aws_unsigned_s3_client():
    my_globals.unsigned_s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))

def initialize_aws_regionless_victim_clients(victim_access_key, victim_secret_access_key, victim_session_token):
    if victim_access_key is not None and victim_secret_access_key is not None:
        victim_session = boto3.Session(
            aws_access_key_id=victim_access_key,
            aws_secret_access_key=victim_secret_access_key,
            aws_session_token=victim_session_token
        )
        victim_clients = {
            "sts": victim_session.client("sts"),
            "iam": victim_session.client("iam"),
            "s3": victim_session.client("s3"),
        }
        return victim_session, victim_clients
    else:
        return None, None

def initialize_aws_regionless_attacker_clients(attacker_access_key, attacker_secret_access_key):
    if attacker_access_key is not None and attacker_secret_access_key is not None:
        attacker_session = boto3.Session(
            aws_access_key_id=attacker_access_key,
            aws_secret_access_key=attacker_secret_access_key
        )
        attacker_clients = {
            "sts": attacker_session.client("sts"),
            "iam": attacker_session.client("iam"),
            "s3": attacker_session.client("s3"),
        }
        return attacker_session, attacker_clients
    return None, None