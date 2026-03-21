FROM python:3.12-slim

WORKDIR /app

COPY mcp_service/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY mcp_service /app/mcp_service

EXPOSE 9000

CMD ["python", "-m", "mcp_service.mcp_server"]