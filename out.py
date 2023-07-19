#!/usr/bin/env python3

import json
import sys
import boto3

# Set up the client with the credentials
client = boto3.client('elasticbeanstalk')
# Create the application version
def create_application_version(application_name, version_label, s3_bucket, s3_key):
    client.create_application_version(
        ApplicationName=application_name,
        VersionLabel=version_label,
        SourceBundle={
            'S3Bucket': s3_bucket,
            'S3Key': s3_key
        }
    )

if __name__ == "__main__":
    parsed = json.loads(sys.stdin.read())
    create_application_version(
        parsed['application_name'], 
        parsed['version_label'], 
        parsed['s3_bucket'],
        parsed['s3_key']
    )