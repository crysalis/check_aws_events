AWS Lambda 

python2.7

check ec2 events and send notifications at slack channel

uses iam roles with permissions:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1498058720000",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstanceStatus",
                "ec2:DescribeInstances"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}