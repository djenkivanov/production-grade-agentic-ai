import functions
import output_classes
from agents import Runner
import local_agents
import asyncio

# async def report_latest_papers(category: str = "cs.AI", papers_count: int = 5) -> str:
#     papers: output_classes.Papers = functions.get_papers(category=category, papers_count=papers_count)

#     interesting_paper = await Runner.run(local_agents.analyst, input=papers.model_dump_json())

#     reports = await asyncio.gather(
#         Runner.run(local_agents.reporter_gpt_4o_mini, input=str(interesting_paper)),
#         Runner.run(local_agents.reporter_gpt_5_4, input=str(interesting_paper)),
#         Runner.run(local_agents.reporter_gpt_5_mini, input=str(interesting_paper))
#     )

#     reasoned_report = await Runner.run(local_agents.reasoning_agent, input=str(reports))
    
#     formatted_report = functions.format_report_to_markdown(reasoned_report.final_output)
    
#     return formatted_report

# CHEAPER TEST
async def report_latest_papers(category: str = "cs.AI", papers_count: int = 5) -> str:
    papers: output_classes.Papers = functions.get_papers(category=category, papers_count=papers_count)

    interesting_paper = await Runner.run(local_agents.analyst, input=papers.model_dump_json())

    reports = await asyncio.gather(
        Runner.run(local_agents.reporter_gpt_4o_mini, input=str(interesting_paper)),
    )

    formatted_report = functions.format_report_to_markdown(reports[0].final_output)
    
    return formatted_report


if __name__ == "__main__":
    import asyncio
    asyncio.run(report_latest_papers())