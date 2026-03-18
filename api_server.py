from fastapi import FastAPI
import workflows

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/report-latest-papers")
async def latest_report(category: str = "cs.AI", papers_count: int = 5):
    return await workflows.report_latest_papers(category=category, papers_count=papers_count)


