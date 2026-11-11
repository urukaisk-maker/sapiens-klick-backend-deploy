FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DATABASE_URL="postgresql://neondb_owner:TU_CONTRASEÑA_REAL@ep-frosty-frost-b2cjrwpd-pooler.c-6.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}