from langchain.messages import HumanMessage, AIMessage, ToolMessage
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from dotenv import load_dotenv
load_dotenv()

model = init_chat_model(
    "deepseek-chat",
    # Kwargs passed to the model:
    temperature=0.7,
    timeout=30,
    max_tokens=1000,
)

def get_weather_tool(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model=model,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    tools=[get_weather_tool],
    system_prompt="You are a helpful assistant",
    response_format=None
)

# Run the agent
raw_response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print(raw_response)

