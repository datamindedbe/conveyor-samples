# Quality Coffee

A sample dbt project used to illustrate some best practices for testing your dbt code using Conveyor.

If you want more background information on different kinds of tests you can use with dbt,
you can refer to blogpost [Testing frameworks in dbt](https://medium.com/datamindedbe/testing-frameworks-in-dbt-3fa8933a5807).


## Getting started 

```bash
make install #This sets up the virtual environment
docker-compose up -d #Sets up a local postgres
```

After that we can run dbt, open the terminal:

```bash
cd dbt
dbt seed # This command can take a while
dbt run
dbt test
```