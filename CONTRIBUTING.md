# Contributing to Conveyor Samples

First off, thank you for considering contributing to the Conveyor Samples repository! We welcome contributions from the community to help showcase the power and flexibility of Conveyor. Your efforts help others learn and integrate Conveyor effectively.

## Context: What are these Samples?

This repository houses a collection of sample projects designed to run on the Conveyor platform. Each sample aims to illustrate:

* **Specific Use Cases:** Demonstrating how Conveyor can solve particular data processing or orchestration problems.
* **Technology Integration:** Providing examples of how to integrate Conveyor with various external technologies, databases, APIs, or cloud services.

A key goal is that **samples should be designed to be usable across different Conveyor tenants** without requiring tenant-specific modifications in the core sample logic. Configuration details (like connection strings or specific bucket names) should be handled through environment variables or Conveyor's configuration mechanisms where possible.

## General Guidelines for New Samples

When creating a new sample, please keep the following principles in mind:

1.  **Keep it Simple:** Samples should be focused and easy to understand. Avoid overly complex architectures or introducing too many technologies at once. The primary goal is to demonstrate a specific Conveyor feature or integration.
2.  **Minimize Infrastructure:** Use minimal external infrastructure. If cloud infrastructure is required:
    * **Shared Infrastructure:** If a piece of infrastructure is low-cost (or free tier eligible) and potentially usable by *multiple* samples (e.g., a standard SQS queue setup pattern, a basic serverless function), consider documenting its setup in a central "Cross-Sample Prerequisites" section (if one exists, or propose creating one).
    * **Sample-Specific Infrastructure:** Any infrastructure needed *only* for your specific sample must be clearly documented within that sample's `README.md`, including setup and teardown instructions.
3.  **Cost-Conscious:** Prefer services with free tiers or low costs for any required cloud infrastructure. Always include cleanup instructions to avoid unexpected charges for users.
4.  **AWS Infrastructure:** When setting up AWS resources is necessary, the default and preferred method is using **AWS CloudFormation**. Provide the template and instructions within the sample's documentation.
5.  **Cross-Tenant Compatibility:** Design the sample so that it doesn't rely on hardcoded values specific to a single Conveyor environment or tenant. Use placeholders or explain how users should configure it for their own environment.
6.  **Documentation is Key:** Every sample *must* have a `README.md` file following the structure outlined below.

## Sample Documentation Structure (`README.md`)

Every sample directory must contain a `README.md` file that adheres strictly to the following format. This ensures consistency and makes it easy for users to run and understand the samples.

```markdown
# NAME_OF_THE_SAMPLE

Provide some context what the sample is about. Explain the use case it demonstrates or the technology integration it showcases.

## Prerequisites

List everything a user needs *before* they can run the Conveyor-specific steps.

### Infra

Describe any infrastructure dependencies (e.g., cloud resources like S3 buckets, RDS databases, SQS queues, external APIs).
* Provide clear, step-by-step instructions on how to set them up.
* If using AWS, provide CloudFormation templates (`.yaml` or `.json`) and instructions on how to deploy them (e.g., `aws cloudformation create-stack ...`).
* Include instructions for **tearing down** this infrastructure later.

### Data

Describe any data dependencies (e.g., sample CSV files, database schemas, required API keys).
* Provide clear instructions on how to acquire or set up this data (e.g., "Download `sample.csv` from [link] and upload it to the S3 bucket created in the Infra step.").
* Specify the format and location expected by the sample.

## Quickstart

Provide the essential commands for a user to get the sample running quickly in a standard Conveyor environment (like a `samples` environment).

1.  Initialize this folder as a project: `conveyor project create --name NAME_OF_THE_SAMPLE` (Replace NAME_OF_THE_SAMPLE)
2.  Build the project: `conveyor build`
3.  Deploy the project to the samples environment: `conveyor deploy --env samples --wait`
4.  *(Add any specific commands needed to trigger or observe the sample, e.g., `conveyor run task <task_name>`, instructions to check output in S3/database)*
5.  Cleanup: *(Provide commands/steps to remove Conveyor resources, e.g., `conveyor project delete --name NAME_OF_THE_SAMPLE --force`)*

## Walkthrough

Provide a more detailed, step-by-step guide through the sample.
* Explain the *why* behind the steps, not just the *how*.
* Describe the components within the sample (e.g., tasks, connections, schedules).
* Elaborate on the data flow or process being demonstrated.
* Explain how to verify the sample ran correctly (e.g., check logs, query data).
* **Crucially, include detailed cleanup steps here**, covering both the Conveyor deployment *and* any external infrastructure or data created in the Prerequisites section. Ensure the user can return their environment to the state it was in before running the sample.
* Close with a conclusion. Provide a short summary of what the user has achieved or learned by completing this sample walkthrough. Briefly reiterate the key Conveyor concepts or integration patterns demonstrated.
```