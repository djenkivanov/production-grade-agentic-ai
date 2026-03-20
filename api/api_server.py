from fastapi import FastAPI, HTTPException
import uuid
from common.custom_classes import ReportRequest
from job_executor import queue_report_job, store_report_job, get_report_job


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/reports")
async def create_report(rr: ReportRequest):    
    job_id = str(uuid.uuid4())
    
    store_report_job(job_id, rr)
    
    queue_report_job(job_id)

    return {
        "job_id": job_id,
        "status": "queued"
    }


@app.get("/reports/{job_id}")
async def get_report(job_id: str):
    return get_report_job(job_id)