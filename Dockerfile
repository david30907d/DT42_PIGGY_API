FROM python:3.7.6-alpine3.11

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apk --update --no-cache add gcc g++ git nginx libffi-dev openssl-dev \
    # 1. if you don't need postgres, remember to remove postgresql-dev and sqlalchemy
    # 2. libffi-dev, openssl-dev is required by poetry
    && pip install --no-cache-dir poetry==1.0.5

WORKDIR /app
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry install --no-interaction --no-ansi --no-dev \
    # Cleaning poetry installation's cache for production:
    && rm -rf "$POETRY_CACHE_DIR" \
    && apk del gcc g++ git \
    && pip uninstall -yq poetry \
    && rm -rf /tmp/* /var/cache/apk/*

COPY project project
COPY tests tests
COPY nginx.conf /etc/nginx/nginx.conf
COPY docker-entrypoint.sh docker-entrypoint.sh
EXPOSE 8000

# Setup ENTRYPOINT
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["server"]