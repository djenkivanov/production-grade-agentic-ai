from mcp.server.fastmcp import FastMCP
import json
import httpx

url = "http://localhost:8000"
mcp = FastMCP("Latest Computer Science Papers Analysis")

@mcp.tool()
async def build_latest_report(category: str = "cs.AI") -> str:
    """
    Analyze computer science papers and return a report.
    """
    with open("arxiv_cs_cat.json", "r") as f:
        categories = json.load(f)
    
    if category not in categories:
        raise ValueError(f"Category '{category}' not found. Available categories: {', '.join(categories)}")
    
    endpoint = f"{url}/report-latest-papers"
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint, params={"category": category})
        
    return response.text

@mcp.tool()
def get_arxiv_categories() -> str:
    """
    Return a list of arXiv computer science categories.
    """
    with open("arxiv_cs_cat.json", "r") as f:
        categories = json.load(f)
    return json.dumps(categories, indent=4)