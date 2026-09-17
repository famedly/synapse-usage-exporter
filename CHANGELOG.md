# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2026-09-17

### Security

- Update base image from the end-of-life `python:3.9` to `python:3.13-slim` and bump all
  dependencies. Closes CVE-2023-41419 (gevent, critical), CVE-2026-7246 (click),
  CVE-2026-28684 (python-dotenv) and CVE-2026-27205 (Flask), and clears the backlog of
  unpatched Debian packages carried by the stale base image.
- Run the container as an unprivileged user (uid 10001) instead of root.

### Miscellaneous Tasks

- Change Docker registry to Harbor
- Rename registry user
- Bump base image and deps

### Upgrade notes

- The container no longer runs as root. Whatever provides `PROMETHEUS_MULTIPROC_DIR` must
  be writable by uid 10001 — in Kubernetes, set `fsGroup: 10001` on the pod security
  context. Without it the container still reports healthy on `/healthz` but rejects every
  usage report with a 500.

## [0.2.0] - 2025-06-19

### Features

- Add observability endpoints

## [0.1.0] - 2025-06-04

### Features

- Add GitHub workflows

### Documentation

- Update info about stats config

### Miscellaneous Tasks

- Format to pass Python Black lints
- Simplify tags in exported metrics
