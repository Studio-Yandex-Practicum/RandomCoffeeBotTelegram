FROM python:3.11

WORKDIR /app

COPY requirements/production.txt .
RUN pip install -r production.txt --no-cache-dir

COPY . .

WORKDIR ./src

CMD ["uvicorn", "core.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
