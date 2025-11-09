
from typing import TypedDict
from langchain.agents import create_agent

from dotenv import load_dotenv
load_dotenv()

class ContactInfo(TypedDict):
    name: str
    email: str
    phone: str


agent = create_agent(model="deepseek-chat", response_format=ContactInfo)

recorded_conversation = """We talked with John Doe. He works over at Example. His number is, let's see, 
five, five, five, one two three, four, five, six seven. Did you get that?
And, his email was john at example.com. He wanted to order 50 boxes of Captain Crunch."""

result = agent.invoke(
    {"messages": [{"role": "user", "content": recorded_conversation}]}
)

print(result["structured_response"])
# {'name': 'John Doe', 'email': 'john@example.com', 'phone': '5551234567'}