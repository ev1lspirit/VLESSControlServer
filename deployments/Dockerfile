FROM python:3.12-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN mkdir -p /app/nginx

COPY source /app/source
COPY logs /app/logs
COPY secrets /app/secrets

CMD ["sh", "-c", "exec python -m source.app"]
