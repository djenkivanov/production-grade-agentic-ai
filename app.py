from fastapi import FastAPI
import workflows
from fastapi.responses import FileResponse
import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/latest-report")
async def latest_report():
    path = await workflows.build_latest_report()
    filename = f"AI_Paper_Report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
    return FileResponse(path, media_type="text/markdown", filename=filename)