# Synapse Usage Exporter

Export the usage statistic of a Synapse homeserver to be scraped by Prometheus.

If you would like to set up your own statistics collection server and send metrics there, you may consider using one of the following known implementations:

* [Matrix.org's Panopticon](https://github.com/matrix-org/panopticon)
* [Famedly's Barad-dûr](https://gitlab.com/famedly/infra/services/barad-dur)

## Motivation

Synapse does not include usage statistics in its prometheus metrics. They can be reported to a HTTP PUT endpoint 5 minutes after startup and from then on at a fixed interval of once every three hours. This simple Flask project offers a HTTP PUT endpoint and holds the most recent received record available to be scraped py Prometheus.

## Environment variables

- `PROMETHEUS_MULTIPROC_DIR` must be set.

Advanced and optional:

- `WERKZEUG_LOG_LEVEL`. Default: `INFO`
- `APP_LOG_LEVEL`. Default: `INFO`

## Usage

```
pip install -r requirements.txt
export PROMETHEUS_MULTIPROC_DIR=/tmp
flask run
```

### With docker

1. Build and run the image with 

```
docker-compose -f docker/docker-compose.yml up --build
```

2. Enable reporting and set the reporting endpoint in Synapse.

```
config.reportStats: true
extraConfig.report_stats_endpoint: <container-ip>:5000/report-usage-stats/push
```

3. Restart Synapse for the changes to take effect and wait at least 5 minutes until the first report is pushed.

4. Configure prometheus to scrape the endpoint with

```
  - job_name: 'synapse-usage'
    static_configs:
      - targets: ['<container-ip>:5000']
```

## License

See [LICENSE.md](LICENSE.md).

__Note:__ This repository is a fork of [loelkes/synapse-usage-exporter](https://github.com/loelkes/synapse-usage-exporter) based on their license ([GNU AGPL](https://github.com/loelkes/synapse-usage-exporter/blob/main/LICENSE.md)).

## Releases

* Change the version in `app/__version__.py`
* Run `pip3 install black ruff` then `python3 -m black --check .` and `python3 -m ruff check .` to validate formatting and linting
* Run `git-cliff --bump`
* Add relevant parts of the git-cliff output to `CHANGELOG.md`
* Create release commit and submit PR: `git commit -m "release: v0.x.x"`
* After PR merge: `git tag -a -s v0.x.x -m "v0.x.x"`


