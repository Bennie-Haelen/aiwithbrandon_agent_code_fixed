import datetime
from google.adk.agents import Agent
from google.adk.tools import google_search

def get_current_time() -> dict:
    """
    Get the current time in the format: YYY-MM-DD HH:MM:SS
    """
    return {
        "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


root_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    description="Tool agent",
    instruction="""
    You are a helpful asssistant that can use the following tools:
    - google_search
    """,
    tools=[get_current_time],
)