from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()

agent = create_agent(
    model="deepseek-chat",
    system_prompt="You are a full-stack comedian",
)

# 1. No Steaming (invoke)
# result = agent.invoke({"messages": [{"role": "user", "content": "Tell me a joke"}]})
# print(result["messages"][1].content)


# 2. Stream = values
# for step in agent.stream(
#     {"messages": [{"role": "user", "content": "Tell me a Dad joke"}]},
#     stream_mode="values",
# ):
#     step["messages"][-1].pretty_print()

# ================================ Human Message =================================

# Tell me a Dad joke
# ================================== Ai Message ==================================

# Why don't skeletons fight each other?

# They don't have the guts.



# 3. Stream = messages
# Messages stream data token by token - the lowest latency possible. 
# This is perfect for interactive applications like chatbots.

# for token, metadata in agent.stream(
#     {"messages": [{"role": "user", "content": "Write me a family friendly poem."}]},
#     stream_mode="messages",
# ):
#     print(f"{token.content}", end="")



# 4. Tools can stream too!

from langgraph.config import get_stream_writer

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    writer = get_stream_writer()
    # stream any arbitrary data
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")
    return f"It's always sunny in {city}!"


agent = create_agent(
    model="deepseek-chat",
    tools=[get_weather],
)

# for chunk in agent.stream(
#     {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
#     stream_mode=["values", "custom"],
# ):
#     print(chunk)

# 5. Try different modes on your own!
# Modify the stream mode and the select to produce different results.

for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode=["values", "custom"],
):
    if chunk[0] == "custom":
        print(chunk[1])

# Looking up data for city: San Francisco
# Acquired data for city: San Francisco