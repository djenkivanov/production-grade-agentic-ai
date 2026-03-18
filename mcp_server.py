from functions import get_arxiv_categories
from fastmcp import FastMCP
import json
import httpx

local_api_url = "http://localhost:8000"
mcp = FastMCP("Latest Computer Science Papers Analysis")

@mcp.tool()
async def start_paper_analysis(category: str = "cs.AI", papers_count: int = 5) -> str:
    f"""
    Start a background job for agents to analyze computer science papers.
    
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
    
    return post_resp.text
        

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

if __name__ == "__main__":
    mcp.run(transport="sse", port=9000)