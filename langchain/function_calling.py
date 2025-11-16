from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.agents.structured_output import ToolStrategy
from langchain_core.messages import ToolMessage
from pydantic import BaseModel


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 25°C"


@tool
def get_call_phrase() -> str:
    """Get a call phrase."""
    return "This is your call phrase!"


@tool
def get_video_phrase() -> str:
    """Get a video phrase."""
    return "This is your video phrase!"


@wrap_tool_call
def handle_tool_errors(request, handler):
    """Handle tool execution errors with custom messages."""
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error occurred: {str(e)}",
            tool_call_id=request.tool_call["id"],
        )


class Phrases(BaseModel):
    call_phrase: str
    video_phrase: str



def main():
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.0,
        max_tokens=1000,
        timeout=30,
    )
    tools = [search, get_weather, get_call_phrase, get_video_phrase]
    system_prompt = "You are a helpful assistant. Be concise and accurate."
    agent = create_agent(
        model=model,
        tools=tools,
        response_format=ToolStrategy(Phrases),
    )

    try:
        user_input = "最近通話した文字起こしと会議を行った文字起こしを取得してください"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]
        response = agent.invoke({"messages": messages})
        print("Agent Response:", response)
    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    main()
