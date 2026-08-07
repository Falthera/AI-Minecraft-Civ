FROM python:3.12-slim

WORKDIR /app

COPY database/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY database/ /app/

CMD ["python", "migrate.py"]
