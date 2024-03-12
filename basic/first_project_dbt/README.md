# First_dbt_project

## Prerequisites

- [dbt](https://docs.getdbt.com/dbt-cli/installation/)
- [pyenv](https://github.com/pyenv/pyenv) (recommended)

## Project Structure

```bash
root/
 |-- dags/
 |   |-- project.py
 |-- models/
 |-- dbt_project.yml
 |-- profiles.yml
 |-- README.md
 |-- Dockerfile 
```

## Concepts

### dbt project structure
Consult the following documentation regarding [best practices for project structure](https://discourse.getdbt.com/t/how-we-structure-our-dbt-projects/355).

### environment variables
It is common practise to pass configuration by [environment variables](https://docs.getdbt.com/reference/dbt-jinja-functions/env_var).
Locally you use a `.env` file to store credentials. 

## Commands
If you have dbt installed locally, you can use the dbt commands from the root of the project.

If you do not have dbt installed locally, you can start a dbt docker container with your local files mounted:
- `make env` to create a local `.env` file
- `make shell` to start a new shell
- `exit` to terminate the container shell

In order to use the `conveyorDbtTaskFactory` in Airflow, you need to have a `manifest.json` file in your dags folder.
You can generate the manifest as follows:
- `make manifest` executes dbt build and copies the `manifest.json` to your dags folder

Consult the [dbt documentation](https://docs.getdbt.com/docs/introduction) for additional commands.