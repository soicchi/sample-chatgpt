FROM python:3.13 AS builder
WORKDIR /opt
RUN --mount=type=bind,source=./requirements.txt,target=/opt/requirements.txt \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim
WORKDIR /opt
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
