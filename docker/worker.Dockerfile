FROM python:3.12-slim

ENV PYTHONUNBUFFERED=TRUE

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY worker worker

COPY simlab-events/ /shared/
RUN pip install /shared/

CMD ["python", "-m", "worker.main"]