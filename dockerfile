FROM ghcr.io/astral-sh/uv:python3.13-trixie

WORKDIR /p2f/api

ADD . .

EXPOSE 8084

ENV PG_USER=value
ENV PG_PASS=value
ENV PG_HOST=value
ENV PG_PORT=value
ENV PG_DB=value
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/ uv sync --locked

ENV PATH="/p2f/api/.venv/bin/:$PATH"

RUN uv pip install -e .

WORKDIR /p2f/api/p2f_api

# CMD ["/bin/bash"]
CMD [ "uvicorn", "--port", "8084", "main:app" ]