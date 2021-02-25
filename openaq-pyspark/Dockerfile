FROM datamindedbe/spark-k8s-glue:v3.0.1-hadoop-3.3.0

WORKDIR /opt/spark/work-dir
USER 0
COPY requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY setup.py setup.py
COPY src ./src
RUN python3 -m pip install . --no-cache-dir
ARG spark_uid=185
USER ${spark_uid}
ENV PYSPARK_PYTHON python3
