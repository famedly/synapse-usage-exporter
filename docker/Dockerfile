# Build stage: uWSGI ships as an sdist only, so it must be compiled. Keeping the
# toolchain here means it never reaches the runtime image.
FROM python:3.13-slim@sha256:9d2e5553305c7c7b0097999bb17187c69b921ccd6bc9d40e4bb5ebe652c00285 AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpcre2-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt ./requirements.txt
COPY docker/requirements.txt ./requirements-docker.txt
RUN pip install --no-cache-dir -r requirements.txt -r requirements-docker.txt

# Runtime stage
FROM python:3.13-slim@sha256:9d2e5553305c7c7b0097999bb17187c69b921ccd6bc9d40e4bb5ebe652c00285

ARG APP_VERSION=latest
ENV APP_VERSION=${APP_VERSION}

ARG BUILD_ID
ENV BUILD_ID=${BUILD_ID}

# libpcre2 is a runtime dependency of the compiled uWSGI binary.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpcre2-8-0 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 10001 --create-home --shell /usr/sbin/nologin app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /usr/src

COPY docker/docker-entrypoint.d /docker-entrypoint.d
COPY docker/docker-entrypoint.sh /docker-entrypoint.sh
COPY docker/wsgi.py .
COPY docker/uwsgi.ini .

COPY app app

# The entrypoint creates this directory at startup, so it must be owned by the
# unprivileged user that will run it.
ENV PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus
RUN mkdir -p ${PROMETHEUS_MULTIPROC_DIR} \
    && chown -R app:app ${PROMETHEUS_MULTIPROC_DIR} /usr/src

USER app

EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/healthz').read()"
ENTRYPOINT [ "/bin/sh", "/docker-entrypoint.sh" ]
