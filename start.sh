#!/bin/bash

# Run Alembic migrations
sleep 5
cd src
uv run alembic upgrade head
cd ..

uv run /src/src/main.py