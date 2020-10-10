# DT42 Piggy API ![Docker Image CI](https://github.com/david30907d/DT42_PIGGY_API/workflows/Docker%20Image%20CI/badge.svg)

This API would connect PostgreSQL and BerryNet inference with Dashboard.

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
    1. Run a PostgreSQL container in local env: `docker run --rm --name postgres -it -e POSTGRES_PASSWORD=postgres -p 5432:5432 -v $(pwd)/fixtures:/tmp postgres:11.9`
    2. Run your Falcon app in local env:
        1. Without Docker
            * `export LOCATION=dev`
            * `gunicorn --threads 2 -b 127.0.0.1:8000 project.app`
        2. Using Docker: `docker run --rm -it -p 8000:8000 dt42_piggy_api_api`
3. Create table in Database:
    ```bash
    docker-compose exec -T postgres sh -c 'psql -U postgres -f /tmp/stored_procedures.sql'
    docker-compose exec -T postgres sh -c 'psql -U postgres -f /tmp/init.sql'
    ```
4. Create User to login:
    * docker-compose version:
        1. `docker-compose exec api bash`
        2. `python -m commands.create_user -u <email> -p`
    * Without Docker: `python -m commands.create_user -u <email> -p`

## API

### Auth
Use JWT to do authentication and authorization

* Get JWT: `curl -XPOST -H "Content-Type: application/json" localhost:<port>/auth -d '{"email":"davidtnfsh@gmail.com", "password": <password>}'`
    ```json
    {"access_token": "<your JWT>", "token_type": "JWT"}
    ```
* Use JWT to access other protected resources:
    * `curl -XGET -H "Authorization: Bearer <your JWT>" locallhost:8000/<routing>`
    ```json
    {"authorized": true}
    ```
### Settings

* Health probe: `curl -XGET -H "Authorization: Bearer <your JWT>" localhost:<port>/settings`
    * Response: `ok`
* Save `settings.json` as local file: `curl -XPOST -H "Authorization: Bearer <your JWT>" -H "Content-Type: application/json" localhost:<port>/settings -d '{"payload":{"placeholder": ""}, "filepath": "./"}'`
    * Response: `{"status": "success"}`

### Dashboard

* Get records for dashboard: `curl -XGET -H "Authorization: Bearer <your JWT>" localhost:<port>/dashboard`
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

### VideoFeed

* Get records for dashboard: `curl -XGET -H "Authorization: Bearer <your JWT>" localhost:<port>/videofeed`
    * Response: stream of image encoding

## Test

Please check [.github/workflows/dockerimage.yml](.github/workflows/dockerimage.yml) for details

## Deploy

1. Get line notify token and assign to `LINE_TOKEN` in `docker-compose.yml`
2. Get Gmail application password and assign it to `GMAIL_TOKEN` in `docker-compose.yml`

## Built with

![falcon](https://19yw4b240vb03ws8qm25h366-wpengine.netdna-ssl.com/wp-content/uploads/falcon-framework-180x120.jpg)