#!/usr/bin/env python3

import json
import os
import sys
import boto3
import mypy_boto3_elasticbeanstalk as elasticbeanstalk


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

    # Get the first command line argument and change the working directory to it
    os.chdir(sys.argv[1])

    # recurse through all directories in the current directory, printing them to stderr
    for root, dirs, files in os.walk("."):
        # Print the file as a full path
        for file in files:
            content = open(os.path.join(root, file)).read()
            print(f"{os.path.join(root, file)}: {content}", file=sys.stderr)
        # Print the directory as a full path
        for dir in dirs:
            print(os.path.join(root, dir), file=sys.stderr)
        
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
