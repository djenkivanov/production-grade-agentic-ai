from sqlalchemy import create_engine, text
import os
import redis.asyncio as redis
from common.custom_classes import ReportRequest

if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

DB_URL = os.environ["DB_URL"]
REDIS_URL = os.environ["REDIS_URL"]
QUEUE_NAME = "job_queue"

engine = create_engine(DB_URL)
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def queue_report_job(job_id: str):
    await redis_client.rpush("job_queue", job_id) # type: ignore

    
def store_report_job(job_id: str, rr: ReportRequest):
    with engine.begin() as conn:
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