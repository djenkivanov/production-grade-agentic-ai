from fastapi import FastAPI, HTTPException
import asyncio
import uuid
import workflows
from common.custom_classes import ReportRequest


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/reports")
async def create_report(rr: ReportRequest):    
    job_id = str(uuid.uuid4())

    workflows.jobs[job_id] = {
        "status": "queued",
        "result": None,
        "error": None,
        "category": rr.category,
        "papers_count": rr.papers_count
    }

    asyncio.create_task(workflows.run_report_job(job_id, rr))

    return {
        "job_id": job_id,
        "status": "queued"
    }


@app.get("/reports/{job_id}")
async def get_report(job_id: str):
    job = workflows.jobs.get(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job_id,
        "status": job["status"],
        "result": job["result"],
        "error": job["error"]
    }