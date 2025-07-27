from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import AgentTool

from .prompts import ROOT_FINANCIAL_AGENT_PROMPT
from .sub_agents import finalise_response_agent

main_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="An helpful assistant that can answer questions and help with any task.",
    instruction=ROOT_FINANCIAL_AGENT_PROMPT,
)

root_agent = SequentialAgent(
    name="root_agent",
    sub_agents=[main_agent, finalise_response_agent],
    description="An helpful assistant that can answer questions and help with any task.",
)
