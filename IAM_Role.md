Create a role in attacker AWS account with this policy configuration.
Note the principal must exist in this AWS account context.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::**********:user/TEST"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

<img width="926" alt="image" src="https://github.com/user-attachments/assets/d7ecdd82-8096-473e-b4e2-f6b3acc9dd3f" />
