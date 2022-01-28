#!/bin/bash

set -e 

PROVIDER_ARN=$(aws iam list-open-id-connect-providers --output json | jq -r ".OpenIDConnectProviderList[0].Arn")

echo "Creating the cloudformation stack"
aws cloudformation create-stack --stack-name datafy-samples \
    --template-body file://cloudformation/samples.yaml\
    --parameters ParameterKey=OIDCProviderArn,ParameterValue=$PROVIDER_ARN\
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

echo "Cloudformation stack created following the rollout until success"
aws cloudformation wait stack-create-complete --stack-name datafy-samples

echo "The cloudformation stack got succesfully created"