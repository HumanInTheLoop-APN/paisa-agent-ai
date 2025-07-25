from google.adk.agents import LlmAgent

from .prompts import ROOT_FINANCIAL_AGENT_PROMPT

root_agent = LlmAgent(
    name="root_agent",
    description="An helpful assistant that can answer questions and help with any task.",
    instruction=ROOT_FINANCIAL_AGENT_PROMPT,
    tools=[],
)
