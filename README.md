# AWS Enumerator

A modular AWS enumeration script for penetration testing and security auditing.  
This tool uses `boto3` to enumerate services like IAM, EC2, S3, Lambda, RDS, and more.

## Features

- Enumerates customer-managed IAM roles and policies
- Lists EC2 instances
- Lists EBS volumes and snapshots
- Lists EBS public snapshots using victim's AWS account ID
- Identifies RDS databases
- Lists Cognito user pools
- Lists SSM parameters, Macie findings, and Secrets Manager secrets
- Lists Lambda functions and invokes them to inspect responses
- Lists S3 buckets, checks for public access, and downloads bucket contents
- Brute-force AWS account ID if a public S3 bucket was found or provided
- Lists Elastic Beanstalk applications
- Lists CodeCommit repositories and enumerates branches for each repository
- Get AWS account ID from an access key

## Setup

1. Clone the repo or unzip the archive.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Fill in `enum_config.json` with AWS credentials and region:

    Below is a smple file. Note that not all fields are required, some are optional.

```json
{
	"victim_access_key": "AKIA3NR******",
	"victim_secret_access_key": "iupVt*********",
	"victim_session_token": "",
	"victim_region": "us-east-1",
	"victim_buckets": [],
	"victim_aws_account_ID": "78501******",
	"attacker_access_key": "AKIAVIE**********",
	"attacker_secret_access_key": "k6UqaX*********",
	"attacker_region": "us-east-1",
	"attacker_IAM_role_name": "IAM*****",
	"attacker_S3_role_arn": "arn:aws:iam::36*******:role/s3enum******"
}
```

4. Create S3 Role on your AWS account as outlined in [S3_Role.md](https://github.com/Gemei/AWS_Enumerator/blob/main/S3_Role.md)

## Usage

Run the enumerator:

```bash
python3 aws_enumerator.py
```

## To-Do

- Add support for attackers to supply their own AWS account credentials, enabling the following black-box capabilities:
  - Brute-force IAM usernames and roles (similar to `iam__enum_users` and `iam__enum_roles` modules in PACU)
- Expand coverage by adding more AWS services and security checks!
