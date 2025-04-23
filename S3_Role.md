On your AWS account go to IAM and create this role.

```json
{
	"Version": "2012-10-17",
	"Statement": {
		"Effect": "Allow",
		"Action": "sts:AssumeRole",
		"Resource": "arn:aws:iam::<your aws account id>:role/s3enum_role"
	}
}
```

Attach the role to a user through group assignment or directly

![image](https://github.com/user-attachments/assets/6258c626-1214-4efe-954e-c6161189230b)

Go to Policies in IAM and create a policy called `s3enum` that allows the `s3:GetObject` and `s3:ListBucket` permissions to the victim bucket, for example `mega-big-tech` bucket.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Enum",
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::*/*"
        },
        {
            "Sid": "Enum1",
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::*"
        }
    ]
}
```

Go to Roles in IAM and create a trust policy called `s3enum_role` and attached it to `s3enum` policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<your aws account id>:user/<your-username>"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

![435479986-de936820-9269-4b0c-b106-a3681bde69b9](https://github.com/user-attachments/assets/0e5af033-0f4b-4978-ba75-bbf84ed5c315)

