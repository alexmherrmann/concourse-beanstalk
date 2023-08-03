# Use the aws cli to deploy to beanstalk
FROM --platform=linux/amd64 alpine:3

# Install jq
RUN apk add --no-cache jq git python3 py3-pip nodejs npm
RUN npm install -g ts-node

RUN mkdir /app
WORKDIR /app

# Install from the package.json
ADD package.json .
RUN npm install

ADD in.ts /opt/resource/in
ADD out.ts /opt/resource/out
ADD check.ts /opt/resource/check

ENTRYPOINT [ "ts-node-esm" ]
