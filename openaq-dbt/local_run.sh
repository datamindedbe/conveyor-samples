#!/usr/bin/env bash

set -e


credentials=$(aws sts assume-role --role-arn arn:aws:iam::130966031144:role/datafy-dp-dev/openaq-dbt-dev --role-session-name test-session | jq -r ".Credentials")
AccessKeyId=$(echo "$credentials" | jq -r ".AccessKeyId")
SecretAccessKey=$(echo "$credentials" | jq -r ".SecretAccessKey")
SessionToken=$(echo "$credentials" | jq -r ".SessionToken")
docker build -it aq:latest
docker run -it -e AWS_ACCESS_KEY_ID=$AccessKeyId -e AWS_SECRET_ACCESS_KEY=$SecretAccessKey -e AWS_SESSION_TOKEN=$SessionToken -e AWS_REGION="us-east-1" -e TARGET="dev" aq:latest