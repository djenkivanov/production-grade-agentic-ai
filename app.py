from fastapi import FastAPI
import workflows
from fastapi.responses import FileResponse
import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/report-latest-papers")
async def latest_report():
    return await workflows.report_latest_papers()