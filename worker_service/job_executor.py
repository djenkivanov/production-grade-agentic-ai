import time
from sqlalchemy import create_engine, text
import os
import redis.asyncio as redis
from worker_service.workflows import report_latest_papers
from common.custom_classes import ReportRequest
import asyncio
from common.tracing import setup_tracing, get_tracer

time.sleep(5)


if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

setup_tracing("backend-worker")
tracer = get_tracer("worker_service")

DB_URL = os.environ["DB_URL"]
REDIS_URL = os.environ["REDIS_URL"]
QUEUE_NAME = "job_queue"

engine = create_engine(DB_URL)
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def process_job(job_id: str):
    with tracer.start_as_current_span("process_job") as span:
        span.set_attribute("component", "job_executor")
        span.set_attribute("job.id", job_id)
        try:
            with tracer.start_as_current_span("set_job_status_as_running"):
                with engine.begin() as conn:
                    conn.execute(
                        text("UPDATE jobs SET status = 'running' WHERE id = :job_id"),
                        {"job_id": job_id}
                    )
                    span.add_event("job_status_updated", {"new_status": "running"})
                    
            with tracer.start_as_current_span("select_job_from_db"):
                with engine.begin() as conn:
                    row = conn.execute(
                        text("SELECT category, papers_count FROM jobs WHERE id = :job_id"),
                        {"job_id": job_id}
                    ).fetchone()
            
            if row is None:
                span.set_attribute("job.found", False)
                span.add_event("job_not_found_in_db")
                return
        
            span.set_attribute("job.found", True)
            
            category, papers_count = row
            span.set_attribute("job.category", category)
            span.set_attribute("job.papers_count", papers_count)

            rr = ReportRequest(category=category, papers_count=papers_count)
            
            with tracer.start_as_current_span("execute_report_workflow") as workflow_span:
                workflow_span.set_attribute("job.category", category)
                workflow_span.set_attribute("job.papers_count", papers_count)
                result = await report_latest_papers(rr)
                
            with tracer.start_as_current_span("completed_job"):
                with engine.begin() as conn:
                    conn.execute(
                        text("UPDATE jobs SET status = 'completed', result = :result, error = NULL WHERE id = :job_id"),
                        {"job_id": job_id, "result": result}
                    )
                    span.set_attribute("job.success", True)
                    span.add_event("job_status_updated", {"new_status": "completed"})
        except Exception as e:
            span.set_attribute("job.success", False)
            span.set_attribute("job.error", str(e))
            span.record_exception(e)
            with tracer.start_as_current_span("failed_job"):
                with engine.begin() as conn:
                    conn.execute(
                        text("UPDATE jobs SET status = 'failed', error = :error WHERE id = :job_id"),
                        {"job_id": job_id, "error": str(e)}
                    )
                    span.add_event("job_status_updated", {"new_status": "failed"})
                    


async def loop() -> None:
    while True:
        result = await redis_client.blpop(QUEUE_NAME, timeout=1) # type: ignore
        if result is None:
            continue

        _, job_id = result
        
        with tracer.start_as_current_span("job_found_in_queue") as span:
            span.set_attribute("job.id", job_id)
            span.set_attribute("queue.name", QUEUE_NAME)
        
        await process_job(job_id)

if __name__ == "__main__":
    asyncio.run(loop())