from agents import Agent, ModelSettings
from dotenv import load_dotenv
import prompts
import output_classes
import agent_tools

load_dotenv()

# Agent Analyst: Analyze the summarized papers and identify the most interesting single paper, 
# then pass the most interesting paper back.
analyst = Agent(
    name="Analyst",
    instructions=prompts.ANALYST,
    model='gpt-4o-mini',
    output_type=output_classes.Paper
)

# 3 reporter agents, each using different models (in practice this would be different LLM providers entirely, but for simplicity
# we'll different models from the same provider), that will each analyze the paper and write a report.

reporter_gpt_4o_mini = Agent(
    name="Reporter GPT-4o Mini",
    instructions=prompts.REPORTER,
    model='gpt-4o-mini',
    tools=[agent_tools.get_paper_contents],
    model_settings=ModelSettings(temperature=0.7, max_tokens=3000),
    output_type=output_classes.Report
)

reporter_gpt_5_4 = Agent(
    name="Reporter GPT-5.4",
    instructions=prompts.REPORTER,
    model='gpt-5.4',
    tools=[agent_tools.get_paper_contents],
    model_settings=ModelSettings(temperature=0.7, max_tokens=3000),
    output_type=output_classes.Report
)

reporter_gpt_5_mini = Agent(
    name="Reporter GPT-5-mini",
    instructions=prompts.REPORTER,
    model='gpt-5-mini',
    tools=[agent_tools.get_paper_contents],
    model_settings=ModelSettings(max_tokens=3000),
    output_type=output_classes.Report
)

# Agent ReasoningAgent: Analyze and refine the final report
reasoning_agent = Agent(
    name="Reasoning Agent",
    instructions=prompts.REASONING_AGENT,
    model='gpt-4o-mini',
    model_settings=ModelSettings(max_tokens=3000),
    output_type=output_classes.Report
)