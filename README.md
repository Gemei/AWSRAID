![banner](https://github.com/user-attachments/assets/bc73c560-d7a3-41cd-9b6d-bad43f67df1f)

# AWSRAID

A modular AWS enumeration tool for penetration testing and security auditing.  
This tool uses `boto3` to list and enumerate services like IAM, EC2, S3, Lambda, RDS, and more.

## Sample Output
![AWSRAID_GIF](https://github.com/user-attachments/assets/b41999e5-f808-43a8-afce-c1c35ef85e65)

## Features
### IAM
#### Users, Groups & Accounts
- List IAM users and groups
- Brute-force usernames for a specified AWS account ID
- Retrieve AWS account ID from an access key

#### Policies & Roles
- List customer-managed IAM roles and policies
- List inline and attached policies for users, groups, and roles
- Brute-force role names for a specified AWS account ID

### AWS Resources
- List EC2 instances, instance information, and userdata
- List EBS volumes and snapshots
- List public EBS snapshots for a given AWS account ID
- Identify RDS databases
- List public RDS snapshots and cluster snapshots
- List Cognito user pools
- List SSM parameters, Macie findings, and Secrets Manager secrets
- List Lambda functions, retrieve configurations, and attempt invocation
- Download Lambda function code
- List S3 buckets, check for public access, and download bucket contents
- Brute-force AWS account ID if a public S3 bucket is found or provided
- List Elastic Beanstalk applications
- List CodeCommit repositories and their branches

## Setup
1. Clone the repo or unzip the archive.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Fill in `enum_config.json` with AWS credentials and region:

    Below is a sample file. Note that not all fields are required, some are optional.

```json
{
	"victim_access_key": "AKIA******",
	"victim_secret_access_key": "iupVt*********",
	"victim_session_token": "",
	"victim_buckets": ["mega-big-tech"],
	"victim_aws_account_ID": "78501******",
	"victim_regions": ["us-east-1","us-east-2"],
	"attacker_access_key": "AKIAVIE**********",
	"attacker_secret_access_key": "k6UqaX*********",
	"attacker_region": "us-east-1",
	"attacker_IAM_role_name": "IAM*****",
	"attacker_S3_role_arn": "arn:aws:iam::36*******:role/s3enum******",
	"user_name_wordlist": "./wordlists/pacu_usernames_word_list.txt",
	"start_username_brute_force": false,
	"role_name_wordlist": "./wordlists/pacu_role_names_word_list.txt",
	"start_role_name_brute_force": false
}
```

4. Create S3 Role on your AWS account as outlined in [S3_Role.md](https://github.com/Gemei/AWSRAID/blob/main/assets/S3_Role.md)
5. Create IAM Role on your AWS account as outlined in [IAM_Role.md](https://github.com/Gemei/AWSRAID/blob/main/assets/IAM_Role.md)

## Usage
_Note: Only tested on Linux and WSL in Windows._

Run the enumerator:

```bash
python3 awsraid.py
```

## Loot and output location
The tool will have a copy of its terminal output located at `./LOOT/AWSRAID_Output.log`

Additionally, If the script successfully downloaded S3 bucket objects and Lambda function code, 
you will find the files in the `./LOOT` directory, located in the script’s base directory.

Finally, all errors will be timestamped and logged in the `./ERROR` directory.

## To-Do
- Generate a report for potential attack paths, e.g. privesc, leaked credentials, ...etc
- Add API Gateway checks
- Add canary detection
- Add S3 bucket object versions listing and download
- Add EC2 launch template enumeration
- Add the option to specify an output file.
- Add multi-threading
- Add better situational exception handling
- Expand coverage by adding more AWS services and security checks!
