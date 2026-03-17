import functions
import output_classes
from agents import Runner
import local_agents

async def build_latest_report():
    return {"Working": "as intended"}
    papers: output_classes.Papers = functions.get_papers()

    interesting_paper = await Runner.run(local_agents.analyst, input=papers.model_dump_json())

    reports = [
        await Runner.run(local_agents.reporter_gpt_4o_mini, input=interesting_paper.final_output.model_dump()),
        await Runner.run(local_agents.reporter_gpt_5_4, input=interesting_paper.final_output.model_dump()),
        await Runner.run(local_agents.reporter_gpt_5_mini, input=interesting_paper.final_output.model_dump())
    ]

    reasoned_report = await Runner.run(local_agents.reasoning_agent, input=[report.final_output.model_dump() for report in reports])
    
    formatted_report = functions.format_report_to_markdown(reasoned_report.final_output)
    
    return formatted_report

if __name__ == "__main__":
    import asyncio
    asyncio.run(build_latest_report())