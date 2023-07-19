#!/usr/bin/env python3

import json
import sys
import boto3


# Create the application version
def create_application_version(
    client, application_name, version_label, s3_bucket, s3_key
):
    client.create_application_version(
        ApplicationName=application_name,
        VersionLabel=version_label,
        SourceBundle={"S3Bucket": s3_bucket, "S3Key": s3_key},
    )


if __name__ == "__main__":
    stdin = sys.stdin.read()
    parsed = json.loads(stdin)
    # Print stdin to stderr
    print(stdin, file=sys.stderr)
    client = boto3.client(
        "elasticbeanstalk",
        aws_access_key_id=parsed["aws_access_key_id"],
        aws_secret_access_key=parsed["aws_secret_access_key"],
    )
    create_application_version(
        parsed["application_name"],
        parsed["version_label"],
        parsed["s3_bucket"],
        parsed["s3_key"],
    )
