from fastmcp import FastMCP
import json
import httpx

local_api_url = "http://localhost:8000"
mcp = FastMCP("Latest Computer Science Papers Analysis")

@mcp.tool(task=True)
async def build_latest_report(category: str = "cs.AI", papers_count: int = 5) -> str:
    f"""
    Analyze computer science papers and return a single report on a specific paper.
    
    Valid categories:
    {get_arxiv_categories()}
    
    Use the category code (e.g., 'cs.AI') and specify the number of papers to analyze (default is 5).
    """
    with open("arxiv_cs_cat.json", "r") as f:
        categories = json.load(f)
    
    if category not in categories.values():
        raise ValueError(f"Category '{category}' not found. Available categories: {', '.join(categories.values())}")
    
    endpoint = f"{local_api_url}/report-latest-papers"
    timeout = httpx.Timeout(600.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(endpoint, params={"category": category, "papers_count": papers_count})
        
    return response.text

@mcp.tool()
def get_arxiv_categories() -> str:
    """
    Return a list of arXiv computer science categories.
    """
    with open("arxiv_cs_cat.json", "r") as f:
        categories = json.load(f)
    return json.dumps(categories, indent=4)

if __name__ == "__main__":
    mcp.run(transport="http", port=9000)