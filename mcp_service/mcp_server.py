from fastmcp import FastMCP
import httpx
from common.tracing import setup_tracing, get_tracer
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
import os

setup_tracing("mcp-server")

if os.getenv("ENV") != "production":
    API_URL = "http://localhost:8000"

tracer = get_tracer("mcp_server")

HTTPXClientInstrumentor().instrument()

API_URL = os.environ["API_URL"]
mcp = FastMCP("Latest Computer Science Papers Analysis")

@mcp.tool()
async def start_paper_analysis(category: str = "cs.AI", papers_count: int = 5) -> str:
    """
    Start a background job for agents to analyze computer science papers.    
    Use the category code (e.g., 'cs.AI', 'cs.CV') and specify the number of papers to analyze.
    """
    with tracer.start_as_current_span("start_paper_analysis") as span:
        span.set_attribute("job.category", category)
        span.set_attribute("job.papers_count", papers_count)
        span.set_attribute("component", "mcp")
        
        async with httpx.AsyncClient() as client:
            post_resp = await client.post(
                f"{API_URL}/reports", 
                json={"category": category, "papers_count": papers_count}
            )
            
        span.set_attribute("http.status_code", post_resp.status_code)
        
        return post_resp.text
        

@mcp.tool()
def get_job(job_id: str):
    """
    Get the status and result of a report generation job by its ID.
    """
    with tracer.start_as_current_span("get_job") as span:
        span.set_attribute("job.id", job_id)
        span.set_attribute("component", "mcp")
        
        response = httpx.get(f"{API_URL}/reports/{job_id}")
        span.set_attribute("http.status_code", response.status_code)
        
        if response.status_code == 404:
            span.set_attribute("job.found", False)
            raise ValueError(f"Job with ID '{job_id}' not found.")
        
        span.set_attribute("job.found", True)
        response.raise_for_status()
        
        return response.json()

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=9000)