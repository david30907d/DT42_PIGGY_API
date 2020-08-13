# Pyproject template [![Build Status](https://travis-ci.com/david30907d/pyproject_template.svg?branch=master)](https://travis-ci.com/github/david30907d/pyproject_template)

## Demo

`docker run --name mysql -e MYSQL_ROOT_PASSWORD=mysql --rm -it -p 3306:3306 mysql:8.0.20`
`curl -XGET localhost:9000`
`curl -XPOST -H "Content-Type: application/json" localhost:9000 -d '{"payload": {"ddd": 2}, "filepath": "333"}'`
<img width="640" src="demo.gif">

This project use several tools, including
* pytest
* isort
* black
* mypy
* bandit
* safety
* pylint
* commitlint

to format our code base and check security issues

## Install

1. Python dependencies:
    1. `virtualenv venv; . venv/bin/activate`
    2. `pip install poetry`
    3. `poetry install`
2. Npm dependencies, for linter, formatter and commit linter (optional):
    1. `brew install npm`
    2. `npm ci`

## How to Develop

1. Commit using commitizen UI: `npm run commit`

    ![img](https://github.com/commitizen/cz-cli/raw/master/meta/screenshots/add-commit.png)
## Run

1. test: `npm run test`
2. Run all linter before commitment would save some effort: `npm run check`
