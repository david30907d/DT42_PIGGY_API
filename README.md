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
    2. Run your Falcon app in local env: `gunicorn -b 127.0.0.1:9000 project.app`

## API

1. Health probe:
    * URI: `curl -XGET localhost:8000/settings`
    * Response: `ok`
2. Save `settings.json` as local file:
    * URI `curl -XPOST -H "Content-Type: application/json" localhost:8000/settings -d '{"payload":{"placeholder": ""}, "filepath": "./"}'`
    * Response: No Response

## Test

Please check [.github/workflows/dockerimage.yml](.github/workflows/dockerimage.yml) for details

## Built with

![falcon](https://www.google.com/url?sa=i&url=https%3A%2F%2Fnordicapis.com%2F8-open-source-frameworks-for-building-apis-in-python%2F&psig=AOvVaw0BuHr0HJFJWF1fGyqp_f3A&ust=1597387643757000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJCGjevKl-sCFQAAAAAdAAAAABAI)