# Use the aws cli to deploy to beanstalk
FROM --platform=linux/amd64 alpine:3

# Install jq
RUN apk add --no-cache jq git aws-cli python3 py3-pip

RUN mkdir /app
WORKDIR /app
# Install our deps
ADD requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

ADD in.py /opt/resource/in
ADD out.py /opt/resource/out
ADD check.py /opt/resource/check
