import time
from sqlalchemy import create_engine, text
import os
import redis.asyncio as redis
from worker_service.workflows import report_latest_papers
from common.custom_classes import ReportRequest
import asyncio

time.sleep(5)

if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

DB_URL = os.environ["DB_URL"]
REDIS_URL = os.environ["REDIS_URL"]
QUEUE_NAME = "job_queue"

engine = create_engine(DB_URL)
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def process_job(job_id: str):
    with engine.begin() as conn:
        conn.execute(
            text("UPDATE jobs SET status = 'running' WHERE id = :job_id"),
            {"job_id": job_id}
        )
        
        row = conn.execute(
            text("SELECT category, papers_count FROM jobs WHERE id = :job_id"),
            {"job_id": job_id}
        ).fetchone()
        
        if row is None:
            return
        
        category, papers_count = row
        rr = ReportRequest(category=category, papers_count=papers_count)
        
        try:
            await report_latest_papers(rr)
            with engine.begin() as conn:
                conn.execute(
                    text("UPDATE jobs SET status = 'completed' WHERE id = :job_id"),
                    {"job_id": job_id}
                )
        except Exception as e:
            with engine.begin() as conn:
                conn.execute(
                    text("UPDATE jobs SET status = 'failed', error = :error WHERE id = :job_id"),
                    {"job_id": job_id, "error": str(e)}
                )


async def loop() -> None:
    while True:
        result = await redis_client.blpop(QUEUE_NAME, timeout=1) # type: ignore
        if result is None:
            continue

        _, job_id = result
        await process_job(job_id)

if __name__ == "__main__":
    asyncio.run(loop())