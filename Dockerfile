FROM python:3.11

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set up a virtual environment
ENV PATH="/root/.poetry/bin:/venv/bin:$PATH"
RUN python -m venv /venv
ENV s=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE="avikus.settings"
# Copy poetry files and install dependencies
RUN pip install poetry
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy application files
COPY . /app/

# Run the application
EXPOSE 8000

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
