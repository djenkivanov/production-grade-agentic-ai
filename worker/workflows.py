import common.functions as functions
from common.custom_classes import ReportRequest, Papers, Paper
from agents import Runner
import local_agents
import asyncio
import json

jobs: dict[str, dict] = {}

async def report_latest_papers(rr: ReportRequest) -> str:
    papers: Papers = await asyncio.to_thread(functions.get_papers, rr=rr)
    
    interesting_paper_result = await Runner.run(local_agents.analyst, input=papers.model_dump_json())
    interesting_paper_obj: Paper = interesting_paper_result.final_output
    
    paper_contents = functions.get_paper_contents(interesting_paper_obj.url)
    
    reports = await asyncio.gather(
        Runner.run(local_agents.reporter_gpt_4o_mini, input=paper_contents),
        Runner.run(local_agents.reporter_gpt_5_4_nano, input=paper_contents),
        Runner.run(local_agents.reporter_gpt_5_mini, input=paper_contents)
    )

    report_outputs = [r.final_output.model_dump() for r in reports]
    
    reasoned_report = await Runner.run(local_agents.reasoning_agent, input=json.dumps(report_outputs, indent=4))
    
    formatted_report = functions.format_report_to_markdown(reasoned_report.final_output)
    
    return formatted_report


async def run_report_job(job_id: str, rr: ReportRequest):
    jobs[job_id]["status"] = "running"
    try:
        result = await report_latest_papers(rr)
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = result
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)