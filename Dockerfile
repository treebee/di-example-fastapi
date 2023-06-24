FROM python:3.11-bookworm

WORKDIR /app/


COPY constraints.txt pyproject.toml README.md /app/

RUN python -m venv /venv
RUN --mount=source=.git,target=.git,type=bind \
    /venv/bin/pip install -e .[test,postgres,redis] -c constraints.txt

ENV PYTHONPATH=/app/src