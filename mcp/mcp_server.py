from fastmcp import FastMCP
import httpx

local_api_url = "http://localhost:8000"
mcp = FastMCP("Latest Computer Science Papers Analysis")

@mcp.tool()
async def start_paper_analysis(category: str = "cs.AI", papers_count: int = 5) -> str:
    """
    Start a background job for agents to analyze computer science papers.    
    Use the category code (e.g., 'cs.AI', 'cs.CV') and specify the number of papers to analyze.
    """        
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