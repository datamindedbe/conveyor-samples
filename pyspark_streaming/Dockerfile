FROM public.ecr.aws/dataminded/spark-k8s-glue:v3.2.0-2.13-hadoop-3.3.1

ENV PYSPARK_PYTHON python3
WORKDIR /opt/spark/work-dir
USER 0

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
RUN pip3 install -e .
ARG spark_uid=185
USER ${spark_uid}