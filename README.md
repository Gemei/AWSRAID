# AWS Enumerator

A modular AWS enumeration script for penetration testing and security auditing.  
This tool uses `boto3` to enumerate services like IAM, EC2, S3, Lambda, RDS, and more.

## Features

- Enumerates IAM roles and policies
- Lists EC2 instances and EBS volumes/snapshots
- Identifies RDS databases and Cognito user pools
- Scans SSM parameters, Macie findings, Secrets Manager secrets
- Invokes Lambda functions and inspects responses
- Checks public S3 access and downloads bucket contents

## Setup

1. Clone the repo or unzip the archive.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Fill in `enum_config.json` with AWS credentials and region:

```json
{
    "access_key": "YOUR_ACCESS_KEY",
    "secret_access_key": "YOUR_SECRET_ACCESS_KEY",
    "session_token": "OPTIONAL",
    "region": "us-east-1",
    "buckets": ["optional-bucket-name"]
}
```

## Usage

Run the enumerator:

```bash
python aws_enumerator.py
```

## Notes

- More services and checks are planned for the future.
