FROM public.ecr.aws/dataminded/spark-k8s-glue:v3.3.1-hadoop-3.3.4-v2

ENV PYSPARK_PYTHON python3
WORKDIR /opt/spark/work-dir
USER 0

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
RUN pip3 install .
ARG spark_uid=185
USER ${spark_uid}