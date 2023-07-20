#!/usr/bin/env python3

import glob
import json
import os
import sys
import boto3
from botocore.exceptions import ClientError
import mypy_boto3_elasticbeanstalk as elasticbeanstalk


# Create the application version
def create_application_version(
    client: elasticbeanstalk.ElasticBeanstalkClient,
    application_name,
    version_label,
    s3_bucket,
    s3_key,
):
    try:
        client.create_application_version(
            ApplicationName=application_name,
            VersionLabel=version_label,
            SourceBundle={"S3Bucket": s3_bucket, "S3Key": s3_key},
        )
    except ClientError as e:
        # Print the json error message to stderr
        print(f"Error: {json.dumps(e.response)}", file=sys.stderr)
        if(e.response.get("Code", None) == "InvalidParameterValue"):
            print("Application version already exists, continuing...", file=sys.stderr)
        else:
            raise e


if __name__ == "__main__":
    stdin = sys.stdin.read()
    parsed = json.loads(stdin)
    # Print stdin to stderr
    print(f"stdin: {parsed}", file=sys.stderr)

    # Get the first command line argument and change the working directory to it
    os.chdir(sys.argv[1])

    # recurse through all directories in the current directory, printing them to stderr
    # for root, dirs, files in os.walk("."):
    #     # Print the file as a full path
    #     for file in files:
    #         content = open(os.path.join(root, file)).read()
    #         print(f"{os.path.join(root, file)}: {content}", file=sys.stderr)
    #     # Print the directory as a full path
    #     for dir in dirs:
    #         print(os.path.join(root, dir), file=sys.stderr)
        
    client = boto3.client(
        "elasticbeanstalk",
        region_name=parsed["source"]["region"],
        aws_access_key_id=parsed['source']["aws_access_key_id"],
        aws_secret_access_key=parsed['source']["aws_secret_access_key"],
    )

    # Get the version from the first "version" file we see in a subdirectory using a glob
    version = open(glob.glob("*/version", recursive=False)[0]).read().strip()
    
    
    # Get the s3 url from the first "url" file we see in a subdirectory using a glob
    s3url = open(glob.glob("*/url", recursive=False)[0]).read().strip()

    # Remove the initial the https:// from the s3 url
    s3url = s3url.replace("https://", "")
    # Cut the first two directories from the s3 url, which is domain and the bucket name
    s3key = "/".join(s3url.split("/")[2:])



    # Print out our version label and s3 key
    print(f"version: {version} s3key: {s3key}", file=sys.stderr)
    
    # Create the application version
    create_application_version(
        client,
        parsed["params"]["application_name"],
        version,
        parsed["params"]["s3_bucket"],
        s3_key=s3key,
    )

    print(json.dumps({"version": {"ref": f"msai-{version}"}}))
