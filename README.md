# DT42 Piggy API ![Docker Image CI](https://github.com/david30907d/DT42_PIGGY_API/workflows/Docker%20Image%20CI/badge.svg)

This API would connect MySQL and BerryNet inference with Dashboard.

## Install

1. Python dependencies:
    1. `virtualenv venv; . venv/bin/activate`
    2. `pip install poetry`
    3. `poetry install`
2. Npm dependencies, for linter, formatter and commit linter (optional):
    1. `brew install npm`
    2. `npm ci`

## Run

1. Docker-compose version: `docker-compose up`
2. Without docker-compose:
    1. Run a MySQL container in local env: `docker run --name mysql -e MYSQL_ROOT_PASSWORD=mysql --rm -it -p 3306:3306 mysql:8.0.20`
    2. Run your Falcon app in local env:
        1. Without Docker
            * `export STAGING=True`
            * `gunicorn --threads 2 -b 127.0.0.1:8000 project.app`
        2. Using Docker: `docker run --rm -it -p 8000:8000 dt42_piggy_api_api`

## API

### Settings

* Health probe: `curl -XGET localhost:<port>/settings`
    * Response: `ok`
* Save `settings.json` as local file: `curl -XPOST -H "Content-Type: application/json" localhost:<port>/settings -d '{"payload":{"placeholder": ""}, "filepath": "./"}'`
    * Response: `{"status": "success"}`

### Dashboard

* Get records for dashboard: `curl -XGET localhost:<port>/dashboard`
    * Response:
    ```json
    [
        {
            "ID": 1,
            "COMPRESSION": "jpeg",
            "CHANNEL": 0,
            "TIMESTAMP": "2020-08-14 04:12:50",
            "ANNOTATIONS": "[{\"top\": 100, \"left\": 50, \"type\": \"detection\", \"label\": \"person\", \"right\": 128, \"bottom\": 200, \"confidence\": 0.93}]"
        }
    ]
    ```
## Test

Please check [.github/workflows/dockerimage.yml](.github/workflows/dockerimage.yml) for details

## Built with

![falcon](https://19yw4b240vb03ws8qm25h366-wpengine.netdna-ssl.com/wp-content/uploads/falcon-framework-180x120.jpg)