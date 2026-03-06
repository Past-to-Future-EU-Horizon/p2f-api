FROM ghcr.io/astral-sh/uv:python3.13-alpine

# WORKDIR /p2f/api

RUN apk update
RUN apk upgrade
RUN apk add git

ADD . /p2f/api/

EXPOSE 8084

# ENV PG_USER=value
# ENV PG_PASS=value
# ENV PG_HOST=value
# ENV PG_PORT=value
# ENV PG_DB=value

# ENV P2F_EMAIL_SA_USERNAME=value
# ENV P2F_EMAIL_SA_PASSWORD=value
# ENV P2F_EMAIL_SA_PORT=587
# ENV P2F_EMAIL_SA_SERVER=value
# ENV P2F_EMAIL_ADDRESS=value
# ENV P2F_EMAIL_IP_CIDR=value
# ENV P2F_ADMIN_EMAIL_ADDRESS=value
# ENV P2F_TOKEN_TTL=value
# ENV P2F_SALT=value
# ENV P2F_HASH_COUNT=2000
# ENV P2F_TOKEN_DEBUG=False
# ENV P2F_TOKEN_LENGTH=64

ENV UV_LINK_MODE=copy

WORKDIR /p2f/api
RUN --mount=type=cache,target=/root/.cache/ uv sync --no-install-project

ENV PATH="/p2f/api/.venv/bin/.:$PATH"

# # RUN uv sync --locked
# RUN uv build --verbose /p2f/api/.
# RUN uv pip install .
RUN uv sync 

# WORKDIR /p2f/api/p2f_api

# CMD ["/bin/bash"]
CMD [ "uvicorn", "--port", "8084", "p2f_api/main:app" ]
