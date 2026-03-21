from agents import Agent, ModelSettings
import worker_service.prompts
from common.custom_classes import Paper, Report
import os

# production or dev check
if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

# Agent Analyst: Analyze the summarized papers and identify the most interesting single paper, 
# then pass the most interesting paper back.
analyst = Agent(
    name="Analyst",
    instructions=worker_service.prompts.ANALYST,
    model='gpt-4o-mini',
    output_type=Paper
)

# 3 reporter agents, each using different models (in practice this would be different LLM providers entirely, but for simplicity
# we'll different models from the same provider), that will each analyze the paper and write a report.

reporter_gpt_4o_mini = Agent(
    name="Reporter GPT-4o Mini",
    instructions=worker_service.prompts.REPORTER,
    model='gpt-4o-mini',
    model_settings=ModelSettings(max_tokens=3000),
    output_type=Report
)

reporter_gpt_5_4_nano = Agent(
    name="Reporter GPT-5.4-Nano",
    instructions=worker_service.prompts.REPORTER,
    model='gpt-5.4-nano',
    model_settings=ModelSettings(max_tokens=3000),
    output_type=Report
)

reporter_gpt_5_mini = Agent(
    name="Reporter GPT-5-mini",
    instructions=worker_service.prompts.REPORTER,
    model='gpt-5-mini',
    model_settings=ModelSettings(max_tokens=3000),
    output_type=Report
)

# Agent ReasoningAgent: Analyze and refine the final report
reasoning_agent = Agent(
    name="Reasoning Agent",
    instructions=worker_service.prompts.REASONING_AGENT,
    model='gpt-4o-mini',
    model_settings=ModelSettings(max_tokens=3000),
    output_type=Report
)