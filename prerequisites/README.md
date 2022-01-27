# General prerequisites

In order to run the samples, you need some additional prerequisites. Some of these samples require additonal steps to get started, please consult the README in each sample.

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

1. Log in to the CloudFormation console at https://console.aws.amazon.com/cloudformation.

2. Choose `Create stack`.

3. In the `Create Stack` wizard, on the `Specify template` screen, select `Upload a template file` and browse to the file in the cloudformation folder, and then choose Next.

4. On the `Specify stack details` screen, provide the needed input. Then choose Next.

5. On the `Configure statck options` screen, choose Next.

6. On the `Review `screen, verify that all the settings are as you want them, and then choose Create.