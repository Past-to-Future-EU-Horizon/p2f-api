FROM ghcr.io/astral-sh/uv:python3.13-alpine

LABEL org.opencontainers.image.description="Past 2 Future API Container built on the UV package manager alpine image"
LABEL org.opencontainers.image.licenses="GPL3"
LABEL org.opencontainers.image.source="https://ghcr.io/past-to-future-eu-horizon/p2f_api"
LABEL org.opencontainers.image.title="P2F-API"
LABEL org.opencontainers.image.url="https://github.com/Past-to-Future-EU-Horizon/p2f-api"

RUN apk update
RUN apk upgrade
RUN apk add git

ADD . /p2f/api/

EXPOSE 8084

ENV UV_LINK_MODE=copy

WORKDIR /p2f/api
RUN --mount=type=cache,target=/root/.cache/ uv sync --no-install-project

ENV PATH="/p2f/api/.venv/bin/:$PATH"

# # RUN uv sync --locked
RUN uv build --verbose /p2f/api/.
# RUN uv pip install -e .
RUN uv pip install .
# RUN uv sync

WORKDIR /p2f/api/p2f_api

# CMD ["/bin/bash"]
CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "8084", "--log-level", "trace", "--forwarded-allow-ips", "*", "--proxy-headers", "--workers", "1", "main:app" ]
