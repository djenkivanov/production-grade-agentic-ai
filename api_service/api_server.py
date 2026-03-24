from fastapi import FastAPI, HTTPException
import uuid
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from common.custom_classes import ReportRequest
from common.job_functions import store_report_job, queue_report_job, get_report_job
from common.tracing import setup_tracing, get_tracer

setup_tracing("backend-api")
app = FastAPI()

FastAPIInstrumentor.instrument_app(app=app)

tracer = get_tracer("api_server")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/reports")
async def create_report(rr: ReportRequest):
    with tracer.start_as_current_span("create_report") as span:
        job_id = str(uuid.uuid4())
        
        span.set_attribute("job.id", job_id)
        span.set_attribute("job.category", rr.category)
        span.set_attribute("job.papers_count", rr.papers_count)
        span.set_attribute("component", "api")
        
        store_report_job(job_id, rr)
        span.add_event("job_stored_in_postgres")
        
        await queue_report_job(job_id)
        span.add_event("job_stored_in_redis")

        return {
            "job_id": job_id,
            "status": "queued"
        }


@app.get("/reports/{job_id}")
async def get_report(job_id: str):
    with tracer.start_as_current_span("get_report") as span:
        span.set_attribute("job.id", job_id)
        span.set_attribute("component", "api")
        
        job = get_report_job(job_id)
        
        if job is None:
            span.set_attribute("job.found", False)
            raise HTTPException(status_code=404, detail="Job not found")
        
        span.set_attribute("job.found", True)
        return job