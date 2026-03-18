import asyncio
from fastmcp import FastMCP
import json
import httpx

local_api_url = "http://localhost:8000"
mcp = FastMCP("Latest Computer Science Papers Analysis")

@mcp.tool()
async def generate_latest_papers_report(category: str = "cs.AI", papers_count: int = 5) -> str:
    f"""
    Analyze computer science papers, then generate and return a single report on a specific paper.
    
    Valid categories:
    {get_arxiv_categories()}
    
    Use the category code (e.g., 'cs.AI') and specify the number of papers to analyze (default is 5).
    """
    with open("arxiv_cs_cat.json", "r") as f:
        categories = json.load(f)
    
    if category not in categories.values():
        raise ValueError(f"Category '{category}' not found. Available categories: {', '.join(categories.values())}")
        
    async with httpx.AsyncClient() as client:
        post_resp = await client.post(
            f"{local_api_url}/reports", 
            json={"category": category, "papers_count": papers_count}
        )
        
        post_resp.raise_for_status()
        job = post_resp.json()
        job_id = job.get("job_id")
        
        max_attempts = 120
        retry_interval = 2
        
        for _ in range(max_attempts):
            status_resp = await client.get(f"{local_api_url}/reports/{job_id}")
            status_resp.raise_for_status()
            data = status_resp.json()
            
            status = data.get("status")

            if status == "completed":
                return data.get("result")
            
            if status == "failed":
                raise RuntimeError(data.get("error", "Unknown error occurred during report generation."))
            
            await asyncio.sleep(retry_interval)
            
        raise RuntimeError(f"Job {job_id} did not complete within the expected time frame.")

@mcp.tool()
def get_job(job_id: str):
    """
    Get the status and result of a report generation job by its ID.
    """
    response = httpx.get(f"{local_api_url}/reports/{job_id}")
    
    if response.status_code == 404:
        raise ValueError(f"Job with ID '{job_id}' not found.")
    
    response.raise_for_status()
    
    return response.json()

@mcp.tool()
def get_arxiv_categories() -> str:
    """
    Return a list of arXiv computer science categories.
    """
    with open("arxiv_cs_cat.json", "r") as f:
        categories = json.load(f)
    return json.dumps(categories, indent=4)

if __name__ == "__main__":
    mcp.run(transport="sse", port=9000)