# AWS Enumerator

A modular AWS enumeration script for penetration testing and security auditing.  
This tool uses `boto3` to enumerate services like IAM, EC2, S3, Lambda, RDS, and more.

## Features

- Enumerates customer-managed IAM roles and policies
- Lists EC2 instances
- Lists EBS volumes and snapshots (Currently, you would need to manually check for public snapshots using AWS account ID)
- Identifies RDS databases
- Lists Cognito user pools
- Lists SSM parameters, Macie findings, and Secrets Manager secrets
- Lists Lambda functions and invokes them to inspect responses
- Lists S3 buckets, checks for public access, and downloads bucket contents
- Lists Elastic Beanstalk applications
- Lists CodeCommit repositories and enumerates branches for each repository

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
    "region": "DEFAULT_REGION",
    "buckets": ["optional-bucket-name"]
}
```

## Usage

Run the enumerator:

```bash
python3 aws_enumerator.py
```

## Notes

- More services and checks are planned for the future.
