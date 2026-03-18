from fastapi import FastAPI, HTTPException
import asyncio
import uuid
import workflows
import custom_classes

app = FastAPI()

jobs: dict[str, dict] = {}


@app.get("/")
async def root():
    return {"message": "Hello World"}


async def run_report_job(job_id: str, rr: custom_classes.ReportRequest):
    jobs[job_id]["status"] = "running"

    try:
        result = await workflows.report_latest_papers(rr)
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = result
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)


@app.post("/reports")
async def create_report(rr: custom_classes.ReportRequest):
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "queued",
        "result": None,
        "error": None,
        "category": rr.category,
        "papers_count": rr.papers_count
    }

    asyncio.create_task(run_report_job(job_id, rr))

    return {
        "job_id": job_id,
        "status": "queued"
    }


@app.get("/reports/{job_id}")
async def get_report(job_id: str):
    job = jobs.get(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job_id,
        "status": job["status"],
        "result": job["result"],
        "error": job["error"]
    }