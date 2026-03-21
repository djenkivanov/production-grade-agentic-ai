FROM python:3.12-slim

WORKDIR /app

COPY worker_service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY worker_service /app/worker_service
COPY common /app/common

CMD ["python", "-m", "worker_service.job_executor"]