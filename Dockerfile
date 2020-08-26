FROM python:3.7.9-slim-stretch

ARG username
ARG credential
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ nginx libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1-mesa-dev git \
    # 1. if you don't need postgres, remember to remove postgresql-dev and sqlalchemy
    # 2. libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1-mesa-dev are required by opencv
    # 3. git is required by pip install git+https
    && pip install --no-cache-dir poetry==1.0.5

WORKDIR /app
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN pip install git+https://${username}:${credential}@github.com/dt42-ai-solution/dt42-lab-lib.git \
    && pip install git+https://${username}:${credential}@github.com/dt42-ai-solution/dt42-trainer.git \
    # [WORKAROUND] pip install scipy
    && pip install scipy \
    && poetry install --no-interaction --no-ansi --no-dev \
    # Cleaning poetry installation's cache for production:
    && rm -rf "$POETRY_CACHE_DIR" \
    && apt-get remove --auto-remove --purge -y gcc g++ git \
    && apt-get clean \
    && pip uninstall -yq poetry

COPY project project
COPY config config
COPY tests tests
COPY nginx.conf /etc/nginx/nginx.conf
COPY docker-entrypoint.sh docker-entrypoint.sh
EXPOSE 8000

# Setup ENTRYPOINT
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["server"]