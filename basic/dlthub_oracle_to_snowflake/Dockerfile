FROM alpine:latest as oracle

WORKDIR /opt/oracle
# ConnectorX activates the "thick mode" of the oracle client, so one needs some extra libs.
ADD https://download.oracle.com/otn_software/linux/instantclient/instantclient-basiclite-linuxx64.zip ./
RUN unzip instantclient-basiclite-linuxx64.zip && \
    rm -f instantclient-basiclite-linuxx64.zip && \
    cd instantclient* && \
    rm -f *jdbc* *occi* *mysql* *jar uidrvci genezi adrci

FROM docker.io/python:3.12.9-slim-bullseye

COPY --from=ghcr.io/astral-sh/uv:0.6.14 /uv /bin/uv

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      gcc \
      libaio1 \
      unzip \
    ; \
    rm -rf /var/lib/apt/lists/*

COPY --from=oracle /opt/oracle /opt/oracle
RUN echo /opt/oracle/instantclient* > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig

WORKDIR /usr/src/app
# silence warnings about not being able to use hard-links for the cache-mount
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync \
      --frozen \
      --compile-bytecode \
      --link-mode=copy \
      --no-install-project
ADD . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
      --frozen \
      --compile-bytecode \
      --link-mode=copy

CMD  ["uv", "run", "./src/dlt_example/app.py", "full"]
