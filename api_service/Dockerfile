FROM python:3.12-slim

WORKDIR /app

COPY api_service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY api_service /app/api_service
COPY common /app/common

EXPOSE 8000

CMD ["uvicorn", "api_service.api_server:app", "--host", "0.0.0.0", "--port", "8000"]