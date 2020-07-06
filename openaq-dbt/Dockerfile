FROM python:3.7-slim

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
RUN pip install -e .

ENTRYPOINT ["app"]
