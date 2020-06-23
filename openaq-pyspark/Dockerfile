FROM datamindedbe/spark-k8s-glue:2.4.3-2.11-hadoop-2.9.2-v2

WORKDIR /app
COPY . .
RUN rm /usr/bin/pip && ln -s pip3.6 /usr/bin/pip
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install -e .

ENV PYSPARK_PYTHON python3