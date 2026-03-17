from fastapi import FastAPI
import workflows

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/latest-report")
async def latest_report():
    return await workflows.build_latest_report()