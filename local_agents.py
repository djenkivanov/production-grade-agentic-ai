from agents import Agent, Runner
from dotenv import load_dotenv
import os
import prompts
import output_classes

load_dotenv()

# Agent Summarizer: Summarize the papers received from Scraper with key points and insights.
summarizer = Agent(
    name="Summarizer",
    instructions=prompts.PROMPT_SUMMARIZER,
    model='gpt-4o-mini',
    output_type=output_classes.Summaries
)


# Agent Analyst: Analyze the summarized papers and identify the most interesting single paper, 
# then pass a small summary and link to the paper.

# Agent Ensembler: Using the link to the paper, extract the full text and infer multiple LLMs to analyze the paper and write a 
# comprehensive summary of the paper, including key points, insights, and potential implications for the field.

# Agent ResponsibleAgent: Analyze the summaries provided from the different LLMs and write a final comprehensive summary of the paper,
# while removing biased, hallucinated or inaccurate information and ensuring final summary is accurate and unbiased by cross-referencing
# the summaries provided by the different LLMs and keeping only the most accurate and reliable information.