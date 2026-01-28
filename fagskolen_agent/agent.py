from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

MCP_SERVER = "http://127.0.0.1:8000/mcp"

toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(    
        url=MCP_SERVER,     
        #headers={"Authorization": "Bearer your-auth-token"}
    ),
)

retriver_agent = Agent(
    model='gemini-2.5-flash',
    name='retriver_agent',
    description="Retrives information about the study programs and courses available at Fagskolen i Viken",
    instruction="You are responsible for retriving information about the study programs and courses at Fagskolen i Viken. \
        You can only retrieve the requested information using the provided tools. \
        Use the get_datafields tool to get the names of the available datafields for a study program. \
        Use the get_datafields_values tool to get more information about a study. \
        Do not respond to other requests. \
        Return the information in a understandable format for a LLM.",
    tools=[toolset],
    )

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Answers questions from potential students",
    instruction="You are a helpful assistant that answer questions about Fagskolen i Viken. \
        You can use the retriver_agent subagent to retrieve information about the study programs and courses at Fagskolen. \
        Do not answer other qustions.",
    sub_agents=[retriver_agent],
    )

