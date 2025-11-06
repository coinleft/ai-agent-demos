from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

agent = create_agent(
    model="deepseek-chat", 
    system_prompt="You are a full-stack comedian"
)

human_msg = HumanMessage("Hello, how are you?")

# print(human_msg)
# content='Hello, how are you?' additional_kwargs={} response_metadata={}

# result = agent.invoke({"messages": [human_msg]})
# print(result)
# print(result["messages"][-1].pretty_print())
# print(type(result["messages"][-1]))

# for msg in result["messages"]:
#     print(f"{msg.type}: {msg.content}\n")