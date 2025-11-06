from langchain_deepseek import ChatDeepSeek
import asyncio

model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # api_key="...",
    # other params...
)

messages = [
    ("system", "You are a helpful translator. Translate the user sentence to Chinese."),
    ("human", "I love programming."),
]

#  1. 简单调用
# res = model.invoke(messages)
# print(res)

# 2. 流式调用
# for chunk in model.stream(messages):
#     print(chunk.text, end="")


# 3. 异步调用
# async def getRes():
#     res = await model.ainvoke(messages)
#     print(res)

# asyncio.run(getRes())

from pydantic import BaseModel, Field

class GetWeather(BaseModel):
    '''Get the current weather in a given location'''
    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")

class GetPopulation(BaseModel):
    '''Get the current population in a given location'''
    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")

model_with_tools = model.bind_tools([GetWeather, GetPopulation])
ai_msg = model_with_tools.invoke("Which city is hotter today and which is bigger: LA or NY?")
print(ai_msg)

