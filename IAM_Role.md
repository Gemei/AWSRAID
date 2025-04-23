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

