FROM docker.io/python:3.12.9-slim-bullseye

COPY --from=ghcr.io/astral-sh/uv:0.6.14 /uv /bin/uv

WORKDIR /app

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      gcc \
    ; \
    rm -rf /var/lib/apt/lists/*

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

CMD  ["uv", "run", "sqlmesh", "plan", "--auto-apply"]