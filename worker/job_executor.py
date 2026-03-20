import time
from sqlalchemy import create_engine, text
import os
import redis.asyncio as redis
from workflows import report_latest_papers
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


def queue_report_job(job_id: str):
    redis_client.rpush("job_queue", job_id)

    
def store_report_job(job_id: str, rr: ReportRequest):
    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO jobs (id, status, category, papers_count)
                VALUES (:id, :status, :category, :papers_count)
            """),
            {
                "id": job_id,
                "status": "queued",
                "category": rr.category,
                "papers_count": rr.papers_count
            }
        )


def get_report_job(job_id: str):
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT id, status, result, error FROM jobs WHERE id = :job_id"),
            {"job_id": job_id}
        ).fetchone()
        
        if row is None:
            return None
        
        return {
            "id": row[0],
            "status": row[1],
            "result": row[2],
            "error": row[3]
        }


async def loop() -> None:
    while True:
        result = await redis_client.blpop(QUEUE_NAME, timeout=1) # type: ignore
        if result is None:
            continue

        _, job_id = result
        await process_job(job_id)

if __name__ == "__main__":
    asyncio.run(loop())