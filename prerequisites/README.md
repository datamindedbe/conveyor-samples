# General prerequisites

In order to run the samples, you need some additional prerequisites. Some of these samples require additional steps to get started, please consult the README in each sample.

## VSCode 

When running in Gitpod, you can skip this step.

[Visual Studio Code](https://code.visualstudio.com/) is a code editor with many great features. We also recommend to at least install the following extensions:

- [Terminal](https://marketplace.visualstudio.com/items?itemName=formulahendry.terminal)
- [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)
- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)


## AWS CLI

When running in Gitpod, the AWS CLI will already be installed. You will still need to configure it to access your AWS account.

Follow the instructions to install and configure the AWS CLI on your machine: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html. 


## AWS infrastructure

We will use cloudformation to setup some additonal infrastructure.
We will create an S3 bucket that we use for all the samples, and we will create a role that can use the bucket.
To create the stack run the install.sh script:

```bash
./install.sh
```