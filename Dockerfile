FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV PYTHONPATH /src

WORKDIR /src

# Кэшируем для ускорения CI / CD
COPY ./pyproject.toml ./uv.lock /src/
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-install-project --no-dev


COPY . /src
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev


ENV PATH="/src/.venv/bin:$PATH"


RUN chmod +x /src/start.sh
RUN sed -i 's/\r$//' /src/start.sh  && chmod +x /src/start.sh

ENTRYPOINT ["/src/start.sh"]
