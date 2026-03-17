import functions
import output_classes
from agents import Runner
import local_agents

async def report_latest_papers() -> str:
    papers: output_classes.Papers = functions.get_papers()

    interesting_paper = await Runner.run(local_agents.analyst, input=papers.model_dump_json())

    reports = [
        await Runner.run(local_agents.reporter_gpt_4o_mini, input=str(interesting_paper)),
        await Runner.run(local_agents.reporter_gpt_5_4, input=str(interesting_paper)),
        await Runner.run(local_agents.reporter_gpt_5_mini, input=str(interesting_paper))
    ]

    reasoned_report = await Runner.run(local_agents.reasoning_agent, input=str(reports))
    
    formatted_report = functions.format_report_to_markdown(reasoned_report.final_output)
    
    return formatted_report


if __name__ == "__main__":
    import asyncio
    asyncio.run(report_latest_papers())