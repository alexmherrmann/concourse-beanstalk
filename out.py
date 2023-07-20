#!/usr/bin/env python3

import json
import sys
import boto3
try:
    import mypy_boto3_elasticbeanstalk as elasticbeanstalk
except ImportError:
    pass


# Create the application version
def create_application_version(
    client: elasticbeanstalk.ElasticBeanstalkClient,
    application_name,
    version_label,
    s3_bucket,
    s3_key,
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
    print(f"stdin: {parsed}", file=sys.stderr)
    client = boto3.client(
        "elasticbeanstalk",
        region_name=parsed["region"],
        aws_access_key_id=parsed["aws_access_key_id"],
        aws_secret_access_key=parsed["aws_secret_access_key"],
    )
    create_application_version(
        client,
        parsed["application_name"],
        parsed["version_label"],
        parsed["s3_bucket"],
        parsed["s3_key"],
    )
