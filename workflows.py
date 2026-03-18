import functions
import custom_classes
from agents import Runner
import local_agents
import asyncio

async def report_latest_papers(rr: custom_classes.ReportRequest) -> str:
    papers: custom_classes.Papers = await asyncio.to_thread(functions.get_papers, rr=rr)
    
    interesting_paper = await Runner.run(local_agents.analyst, input=papers.model_dump_json())

    reports = await asyncio.gather(
        Runner.run(local_agents.reporter_gpt_4o_mini, input=str(interesting_paper)),
        Runner.run(local_agents.reporter_gpt_5_nano, input=str(interesting_paper)),
        Runner.run(local_agents.reporter_gpt_5_mini, input=str(interesting_paper))
    )

    reasoned_report = await Runner.run(local_agents.reasoning_agent, input=str(reports))
    
    formatted_report = functions.format_report_to_markdown(reasoned_report.final_output)
    
    return formatted_report

# CHEAPER TEST
# async def report_latest_papers(rr: custom_classes.ReportRequest) -> str:
#     papers: custom_classes.Papers = functions.get_papers(category=rr.category, papers_count=rr.papers_count)

#     interesting_paper = await Runner.run(local_agents.analyst, input=papers.model_dump_json())

#     reports = await asyncio.gather(
#         Runner.run(local_agents.reporter_gpt_4o_mini, input=str(interesting_paper)),
#     )

#     formatted_report = functions.format_report_to_markdown(reports[0].final_output)
    
#     return formatted_report
